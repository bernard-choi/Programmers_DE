## Question2

- Gross revenue가 가장 큰 UserID 10개 찾기
  - Gross revenue는 refund 포함한 매출


```sql
  SELECT userid,
         sum(amount) 
  FROM   raw_data.session_transaction AS st
         LEFT JOIN raw_data.user_session_channel AS sc
                ON st.sessionid = sc.sessionid
  GROUP  BY 1
  ORDER  BY 2 DESC;
  ```
