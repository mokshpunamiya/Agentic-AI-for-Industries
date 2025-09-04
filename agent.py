import json
import time
import streamlit as st
from openai import OpenAI


class AgentSystem:
    """Agent system for analyzing PSU data"""

    # Define agent prompts with specific roles
    AGENT_PROMPTS = {
        "analyst": """You are a financial analysis AI for the Ministry of Industries of India. 
You analyze Public Sector Undertaking (PSU) data to provide insights.

INSTRUCTIONS:
1. First understand the user's query and what data is needed to answer it
2. Collect all necessary data using the available tools
3. Provide a clear, concise analysis based on the data
4. Be direct and specific with your insights
5. Format your response with markdown for better readability
6. Highlight critical findings with bullet points
7. Never ask if the user wants more information

TOOLS:
When you need data, output a JSON tool call between <TOOL> and </TOOL> tags:

<TOOL>
{
    "tool": "tool_name",
    "parameters": {"param1": "value1"}
}
</TOOL>

Available tools:
- get_dataset_overview: Gets a high-level overview of the entire dataset (no parameters)
- get_psu_data: Get data for a PSU (parameters: psu_name)
- get_sector_data: Get data for a sector (parameters: sector)
- analyze_psu: Analyze a PSU's performance (parameters: psu_name)
- compare_with_sector: Compare a PSU with sector averages (parameters: psu_name)
- identify_top_performers: Find top PSUs by metric (parameters: sector, metric, top_n)
- analyze_sector: Analyze a sector's performance (parameters: sector)

Example of using a tool:
<TOOL>
{
    "tool": "analyze_psu",
    "parameters": {"psu_name": "PSU_1"}
}
</TOOL>
""",

        "policy": """You are a policy drafting AI for the Ministry of Industries of India.
Your job is to create actionable policy recommendations for PSUs (Public Sector Undertakings).

INSTRUCTIONS:
1. First understand what policy guidance is needed and what data will inform it
2. Collect all necessary data using the available tools
3. Draft clear, specific policy recommendations based on the data
4. Structure recommendations by priority (High/Medium/Low)
5. Use numbered lists for specific action items
6. Include implementation steps where relevant
7. Be direct and specific with recommendations

TOOLS:
When you need data, output a JSON tool call between <TOOL> and </TOOL> tags:

<TOOL>
{
    "tool": "tool_name",
    "parameters": {"param1": "value1"}
}
</TOOL>

Available tools:
- get_dataset_overview: Gets a high-level overview of the entire dataset (no parameters)
- get_psu_data: Get data for a PSU (parameters: psu_name)
- get_sector_data: Get data for a sector (parameters: sector)
- analyze_psu: Analyze a PSU's performance (parameters: psu_name)
- compare_with_sector: Compare a PSU with sector averages (parameters: psu_name)
- identify_top_performers: Find top PSUs by metric (parameters: sector, metric, top_n)
- analyze_sector: Analyze a sector's performance (parameters: sector)

Example of using a tool:
<TOOL>
{
    "tool": "analyze_psu",
    "parameters": {"psu_name": "PSU_1"}
}
</TOOL>
"""
    }

    def __init__(self, api_key, tools):
        self.llm_client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        self.tools = tools
        self.model = "openai/gpt-4o-mini"
        self.max_iterations = 3

        # Tool mapping for execution
        self.tool_map = {
            "get_dataset_overview": self.tools.get_dataset_overview,
            "get_psu_data": self.tools.get_psu_data,
            "get_sector_data": self.tools.get_sector_data,
            "analyze_psu": self.tools.analyze_psu,
            "compare_with_sector": self.tools.compare_with_sector,
            "identify_top_performers": self.tools.identify_top_performers,
            "analyze_sector": self.tools.analyze_sector
        }

    def process_query(self, query, agent_type="analyst"):
        """Process a user query with real-time status updates"""
        # Set up Streamlit placeholders for live updates
        response_container = st.empty()
        status_log = st.status(f"Processing {agent_type} query...")
        status_log.update(
            label=f"Initializing {agent_type} analysis...", state="running")

        try:
            # Initialize conversation context
            context = [
                {"role": "system", "content": self.AGENT_PROMPTS[agent_type]},
                {"role": "user", "content": query}
            ]

            # Initialize collected data for global context
            collected_data = {
                "tools_used": [],
                "dataset_context": None,
                "entity_data": {}
            }

            # First get dataset overview for global context
            with status_log.container():
                st.write("🔎 Getting dataset overview...")
                dataset_overview = self.tools.get_dataset_overview()
                collected_data["dataset_context"] = dataset_overview
                overview_msg = f"""
                Here's an overview of the dataset:
                - {dataset_overview['psu_count']} PSUs across {dataset_overview['sector_count']} sectors
                - Data from {dataset_overview['year_range']}
                - In the latest year ({dataset_overview['latest_year']}), there are {dataset_overview['profitable_psus']} profitable PSUs and {dataset_overview['loss_making_psus']} loss-making PSUs
                """
                context.append({"role": "user", "content": overview_msg})

            # Track iterations
            iteration = 0
            final_response = None

            # Main processing loop
            while iteration < self.max_iterations:
                iteration += 1
                status_log.update(
                    label=f"Iteration {iteration}/{self.max_iterations}", state="running")

                with status_log.container():
                    st.write(f"🧠 Analyzing query and planning response...")
                    start_time = time.time()

                    # Generate LLM response
                    response = self.llm_client.chat.completions.create(
                        model=self.model,
                        messages=context,
                        temperature=0.3
                    )

                    response_text = response.choices[0].message.content
                    context.append(
                        {"role": "assistant", "content": response_text})

                    st.write(
                        f"✅ Analysis completed in {time.time()-start_time:.1f}s")

                    # Parse tool calls
                    tool_calls = self._parse_tool_calls(response_text)

                    # If no more tool calls, we have the final response
                    if not tool_calls:
                        final_response = response_text
                        break

                    # Execute tools
                    for call in tool_calls:
                        tool = call["tool"]
                        params = call["params"]

                        st.write(f"⚙️ Getting data: {tool} {params}")
                        tool_start = time.time()

                        try:
                            if tool in self.tool_map:
                                result = self.tool_map[tool](**params)
                                # Track used tools and results
                                collected_data["tools_used"].append({
                                    "tool": tool,
                                    "params": params,
                                    "result_summary": self._summarize_result(result)
                                })

                                # Store data by entity (PSU or sector)
                                if "psu_name" in params:
                                    collected_data["entity_data"][params["psu_name"]] = result
                                elif "sector" in params:
                                    collected_data["entity_data"][params["sector"]] = result

                                result_str = json.dumps(result, indent=2)
                                context.append({
                                    "role": "user",
                                    "content": f"TOOL RESULT ({tool}): {result_str}"
                                })
                            else:
                                error_msg = f"Unknown tool: {tool}"
                                context.append({
                                    "role": "user",
                                    "content": f"TOOL ERROR: {error_msg}"
                                })
                        except Exception as e:
                            error_msg = f"Tool execution error: {str(e)}"
                            context.append({
                                "role": "user",
                                "content": f"TOOL ERROR: {error_msg}"
                            })

                        st.write(
                            f"⏱️ Data retrieved in {time.time()-tool_start:.1f}s")

            # If we hit max iterations, get final synthesis
            if final_response is None:
                status_log.update(
                    label="Generating final analysis...", state="running")
                # Add a final synthesis message with collected data context
                synthesis_request = f"""
                Based on all the data collected, please provide your final analysis and recommendations. 
                Be concise and direct. Focus on the most important insights and actionable recommendations.
                
                Summary of tools used: {', '.join([t['tool'] for t in collected_data['tools_used']])}
                """
                context.append({"role": "user", "content": synthesis_request})

                # Generate final response
                response = self.llm_client.chat.completions.create(
                    model=self.model,
                    messages=context,
                    temperature=0.3
                )

                final_response = response.choices[0].message.content

            # Clean and display final response
            clean_response = self._clean_response(final_response)
            status_log.update(label="Analysis complete", state="complete")
            response_container.markdown(clean_response)

            return clean_response

        except Exception as e:
            status_log.update(label="Analysis failed", state="error")
            error_msg = f"Error processing query: {str(e)}"
            st.error(error_msg)
            return error_msg

    def _parse_tool_calls(self, text):
        """Extract tool calls from LLM response"""
        tool_calls = []
        if "<TOOL>" not in text:
            return []

        tool_blocks = text.split("<TOOL>")[1:]
        for block in tool_blocks:
            if "</TOOL>" not in block:
                continue

            try:
                json_str = block.split("</TOOL>")[0].strip()
                tool_data = json.loads(json_str)
                tool_calls.append({
                    "tool": tool_data["tool"],
                    "params": tool_data.get("parameters", {})
                })
            except json.JSONDecodeError:
                continue

        return tool_calls

    def _clean_response(self, text):
        """Clean response by removing tool calls and closing statements"""
        # Remove tool calls
        if "<TOOL>" in text:
            parts = text.split("<TOOL>")
            clean_parts = [parts[0]]

            for part in parts[1:]:
                if "</TOOL>" in part:
                    after_tool = part.split("</TOOL>", 1)[1]
                    if after_tool.strip():
                        clean_parts.append(after_tool)

            text = "".join(clean_parts)

        # Remove common closing statements
        closings = [
            "would you like me to elaborate",
            "let me know if you need any clarification",
            "is there anything specific you'd like me to explain",
            "do you need any additional information",
            "would you like more details on",
            "please let me know if you have any questions",
            "I hope this analysis helps"
        ]

        text_lower = text.lower()
        for closing in closings:
            if closing in text_lower:
                # Find the sentence containing the closing
                sentences = text.split(". ")
                for i, sentence in enumerate(sentences):
                    if closing in sentence.lower():
                        # Remove this and all subsequent sentences
                        text = ". ".join(
                            sentences[:i]) + ("." if i > 0 else "")
                        break

        return text.strip()

    def _summarize_result(self, result):
        """Create a short summary of a tool result"""
        if isinstance(result, dict):
            if "error" in result:
                return f"Error: {result['error']}"
            elif "psu_name" in result:
                return f"Data for {result['psu_name']}"
            elif "sector" in result:
                return f"Data for {result['sector']} sector"
            elif "metric" in result:
                return f"Top performers by {result['metric']}"
            else:
                return "Data retrieved successfully"
        elif isinstance(result, list):
            return f"Retrieved {len(result)} records"
        else:
            return "Data retrieved"
