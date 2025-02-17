with ThreadPoolExecutor(max_workers=2) as executor:
    future_count = executor.submit(lambda: execute_query(st.session_state.pre_result), conn)
    future_data = executor.submit(lambda: execute_query(st.session_state.sql_query), conn)

    result = future_count.result()
    data = future_data.result()
