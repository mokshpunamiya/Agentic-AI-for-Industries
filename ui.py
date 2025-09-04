import streamlit as st


class PSUInterface:
    """Streamlit interface for PSU analysis with enhanced UX"""

    def __init__(self, df, agent_system):
        self.df = df
        self.agent_system = agent_system
        self.psu_names = sorted(df['PSU_Name'].unique())
        self.sectors = sorted(df['Sector'].unique())
        self._prepare_session_state()

    def _prepare_session_state(self):
        if 'query' not in st.session_state:
            st.session_state.query = ""
        if 'selected_psu' not in st.session_state:
            st.session_state.selected_psu = "All PSUs"
        if 'selected_sector' not in st.session_state:
            st.session_state.selected_sector = "All Sectors"

    def run(self):
        """Main UI rendering function"""
        # st.set_page_config(page_title="PSU Analysis System", layout="wide")
        st.title("Ministry of Industries Agentic AI System")
        st.markdown("---")

        # Main layout columns
        control_col, analysis_col = st.columns([1, 3], gap="large")

        with control_col:
            self._render_controls()

        with analysis_col:
            self._render_analysis_area()

        self._render_dataset_overview()

    def _render_controls(self):
        """Render the left control panel"""
        with st.container(border=True):
            st.markdown("### 🔍 Analysis Configuration")
            agent_type = st.radio(
                "**Analysis Mode:**",
                ["Analyst", "Policy"],
                index=0,
                help="Choose between detailed analysis or policy recommendations"
            )

            st.markdown("---")
            self._render_psu_selection()
            self._render_sector_selector()
            st.markdown("---")
            self._render_quick_actions(agent_type)

    def _render_psu_selection(self):
        """Render PSU selection with dynamic sector detection"""
        st.session_state.selected_psu = st.selectbox(
            "**Select PSU:**",
            ["All PSUs"] + self.psu_names,
            index=0,
            help="Select specific PSU or analyze all"
        )

        # Show detected sector when single PSU is selected
        if st.session_state.selected_psu != "All PSUs":
            sector = self._get_psu_sector(st.session_state.selected_psu)
            st.markdown(f"**Detected Sector:** {sector}")
            st.session_state.selected_sector = sector  # Auto-set sector context

    def _render_sector_selector(self):
        """Conditionally render sector selector based on PSU selection"""
        if st.session_state.selected_psu == "All PSUs":
            st.session_state.selected_sector = st.selectbox(
                "**Filter by Sector:**",
                ["All Sectors"] + self.sectors,
                index=0,
                help="Filter analysis by specific sector"
            )

    def _render_quick_actions(self, agent_type):
        """Render context-aware quick action buttons"""
        st.markdown("### 🚀 Quick Analysis")

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("📊 PSU Overview", use_container_width=True):
                self._trigger_overview_query(agent_type)

        with btn_col2:
            if st.button("📈 Trend Analysis", use_container_width=True):
                self._trigger_trend_query(agent_type)

        if st.session_state.selected_psu == "All PSUs":
            if st.button("🏭 Sector Comparison", use_container_width=True):
                self._trigger_sector_comparison(agent_type)
        else:
            if st.button("📋 Financial Health", use_container_width=True):
                self._trigger_financial_health_query(agent_type)

        if st.button("🏆 Top Performers", use_container_width=True):
            self._trigger_top_performers_query(agent_type)

    def _render_analysis_area(self):
        """Render the main analysis area"""
        with st.container(border=True):
            st.markdown("### 🧠 Analysis Query")

            # Dynamic placeholder based on selection
            placeholder = self._get_query_placeholder()
            query = st.text_area(
                "Enter your analysis query:",
                value=st.session_state.query,
                height=150,
                placeholder=placeholder,
                help="Enter natural language questions or analysis requests"
            )

            st.session_state.query = query

            if st.button("✨ Analyze", type="primary", use_container_width=True):
                if query:
                    self._process_query(query, agent_type="analyst")
                else:
                    st.warning("Please enter a query or use quick actions")

    def _get_query_placeholder(self):
        """Generate contextual query placeholder"""
        base = "Examples:\n- Compare profitability trends between sectors\n- Suggest policy improvements for energy PSUs"

        if st.session_state.selected_psu != "All PSUs":
            sector = self._get_psu_sector(st.session_state.selected_psu)
            return f"E.g., 'Performance trends of {st.session_state.selected_psu}'\n- Financial health assessment\n- {sector} sector comparison\n{base}"

        if st.session_state.selected_sector != "All Sectors":
            return f"E.g., 'Growth patterns in {st.session_state.selected_sector} sector'\n- Compare PSUs in this sector\n- Policy recommendations\n{base}"

        return base

    def _trigger_overview_query(self, agent_type):
        """Generate overview query based on context"""
        if st.session_state.selected_psu == "All PSUs":
            query = "Provide comprehensive overview of PSUs"
            if st.session_state.selected_sector != "All Sectors":
                query += f" in {st.session_state.selected_sector} sector"
        else:
            query = f"Detailed analysis of {st.session_state.selected_psu} including sector context"
        # Only update the query text without processing immediately
        st.session_state.query = query
        # Redirect to the right analysis area by just updating session state

    def _trigger_trend_query(self, agent_type):
        """Generate trend analysis query"""
        if st.session_state.selected_psu == "All PSUs":
            query = "Show 5-year performance trends"
            if st.session_state.selected_sector != "All Sectors":
                query += f" for {st.session_state.selected_sector} sector"
        else:
            query = f"Analyze performance trends of {st.session_state.selected_psu} over time"
        # Only update query text without immediate processing
        st.session_state.query = query

    def _trigger_sector_comparison(self, agent_type):
        """Generate sector comparison query"""
        query = "Compare performance metrics across sectors"
        if st.session_state.selected_sector != "All Sectors":
            query = f"Compare PSUs within {st.session_state.selected_sector} sector"
        # Only update query text without immediate processing
        st.session_state.query = query

    def _trigger_financial_health_query(self, agent_type):
        """Generate financial health query"""
        query = f"Analyze financial health indicators for {st.session_state.selected_psu}"
        # Only update query text without immediate processing
        st.session_state.query = query

    def _trigger_top_performers_query(self, agent_type):
        """Generate top performers query"""
        query = "Identify top performing PSUs"
        if st.session_state.selected_sector != "All Sectors":
            query += f" in {st.session_state.selected_sector} sector"
        # Only update query text without immediate processing
        st.session_state.query = query

    def _get_psu_sector(self, psu_name):
        """Get sector for selected PSU"""
        return self.df[self.df['PSU_Name'] == psu_name]['Sector'].values[0]

    def _set_query_and_process(self, query, agent_type):
        """Set query and trigger processing"""
        st.session_state.query = query
        self._process_query(query, agent_type.lower())

    # In the PSUInterface class, modify the _process_query method:

    def _process_query(self, query, agent_type):
        """Process query with contextual information"""
        context = {
            "selected_psu": st.session_state.selected_psu,
            "selected_sector": st.session_state.selected_sector
        }

        self.agent_system.process_query(query, agent_type.lower())

    def _render_dataset_overview(self):
        """Enhanced dataset overview with visual elements"""
        with st.expander("📁 Dataset Summary", expanded=True):
            overview = self.agent_system.tools.get_dataset_overview()

            cols = st.columns([1, 1, 2])
            with cols[0]:
                st.metric("Total PSUs", overview["psu_count"])
                st.metric("Sectors Represented", overview["sector_count"])

            with cols[1]:
                st.metric("Year Coverage", overview["year_range"])
                st.metric("Profitable/Loss Ratio",
                          f"{overview['profitable_psus']} / {overview['loss_making_psus']}")

            with cols[2]:
                st.markdown("**Sector Distribution**")
                # Replace sector_distribution with sector_count
                sector_counts = {s: self.df[self.df['Sector'] == s].shape[0]
                                 for s in self.df['Sector'].unique()}
                st.bar_chart(sector_counts)

            st.caption(
                f"Latest data from {overview['latest_year']} | Total Revenue: ₹{overview['total_revenue']:,.0f}M")
