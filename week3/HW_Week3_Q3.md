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



## Question3
-  채널별 월 매출액 테이블 만들기
    - session_timestamp, user_session_channel, channel, transaction)
- chnnel에 있는 모든 채널에 대해 구성해야됨(값이 없는 경우라도)
- 아래와 같은 필드로 구성
  - month, channel, uniqueUses, conversionRate(구매사용자/총방문사용자), grossRevenue(Refund포함), netRevenue(Refund제외)

#### 문제1. 값이 없는 경우라도 모든 채널에 대해 병합해야함


```sql
SELECT ts.sessionid,
       Extract(month FROM ts.ts) AS mon,  -- 월만 추출
       st.refunded,
       st.amount,
       usc.userid,
       usc.channel
FROM   raw_data.session_timestamp AS ts --sessionid 를 기준으로 timestanp, user_session_channel, transaction 정보를 합침.
       LEFT JOIN raw_data.session_transaction AS st
              ON ts.sessionid = st.sessionid
       LEFT JOIN raw_data.user_session_channel AS usc
              ON ts.sessionid = usc.sessionid;
```


[ 결과값 ]

![](https://user-images.githubusercontent.com/36406676/89627709-39a5f580-d8d6-11ea-8c60-4d6baf11b0d2.PNG)




```sql
SELECT DISTINCT( channel )
FROM   raw_data.session_timestamp AS ts
       LEFT JOIN raw_data.session_transaction AS st
              ON ts.sessionid = st.sessionid
       LEFT JOIN raw_data.user_session_channel AS usc
              ON ts.sessionid = usc.sessionid;
```

[ 결과값 ] - TIKTOC이 없다.

![](https://user-images.githubusercontent.com/36406676/89628103-c355c300-d8d6-11ea-98fb-6439f977664b.PNG)

```sql

SELECT DISTINCT( ch.channelname )
FROM   raw_data.channel AS ch
       LEFT JOIN raw_data.user_session_channel AS usc -- 실행순서3. channel table에 최종적으로 left join.
              ON ch.channelname = usc.channel
       LEFT JOIN raw_data.session_timestamp AS ts -- 실행순서2
              ON usc.sessionid = ts.sessionid
       LEFT JOIN raw_data.session_transaction AS st -- 실행순서1
              ON usc.sessionid = st.sessionid;

```
[ 결과값 ]

![](https://user-images.githubusercontent.com/36406676/89704611-32432280-d990-11ea-8f9c-969d03409497.PNG)

#### 문제2. Extract / Case  / Nullif


```sql
SELECT ch.channelname AS channel,
       Extract(month FROM ts.ts) AS mon, -- Extract함수를 활용하여 month 추출
       Count(DISTINCT( usc.userid )) AS uniqueUsers,
       Count(DISTINCT CASE -- Case문을 활용하여 amount가 0보다 큰 userid만 추출
                        WHEN amount > 0 THEN userid
                      END) AS paidUsers,
       Round(Cast(paidusers AS FLOAT) / NULLIF(Cast(uniqueusers AS FLOAT), 0) AS conversionRate, -- uniqueusers 가 0인경우 계산X. nullif로 0을 null로 처리.
       Sum(amount) AS grossRevenue,
       Sum(CASE
             WHEN refunded = true THEN 0
             ELSE amount -- refunded가 true인 경우 amount 0 처리
           END) AS netRevenue

FROM   raw_data.channel AS ch
       LEFT JOIN raw_data.user_session_channel AS usc
              ON ch.channelname = usc.channel
       LEFT JOIN raw_data.session_timestamp AS ts
              ON usc.sessionid = ts.sessionid
       LEFT JOIN raw_data.session_transaction AS st
              ON usc.sessionid = st.sessionid
GROUP  BY 1,
          2
ORDER  BY 1,
          2;
```

[ 결과값 ]

![](https://user-images.githubusercontent.com/36406676/89704772-ea24ff80-d991-11ea-83d4-f6e687155e3f.PNG)
