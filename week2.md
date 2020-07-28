## 2주차 과제
---

## MAU(Monthly Active User) 구하기




- left_join, right_join, inner_join 전체 행수 101520 동일. sessionid 동일함 확인
~~~sql
-- left_join
select
	count(*)
from
	RAW_DATA.SESSION_TIMESTAMP as TS
left join RAW_DATA.USER_SESSION_CHANNEL as SC on
	TS.SESSIONID = SC.SESSIONID;

-- right_join
select
	count(*)
from
	RAW_DATA.SESSION_TIMESTAMP as TS
right join RAW_DATA.USER_SESSION_CHANNEL as SC on
	TS.SESSIONID = SC.SESSIONID;

-- inner_join
select
	count(*)
from
	RAW_DATA.SESSION_TIMESTAMP as TS
join RAW_DATA.USER_SESSION_CHANNEL as SC on
	TS.SESSIONID = SC.SESSIONID;
~~~

-  session_timestamp의 ts 컬럼을 YYYY-MM 형식으로 변경

~~~sql
select
	*,
	to_char(TS, 'YYYY-MM')
from
	RAW_DATA.SESSION_TIMESTAMP as TS;
~~~

-  session_timestamp 와 user_session_channel 병합
~~~sql
select
	US.USERID,
	to_char(ST.TS, 'YYYY-MM') as YEAR_MONTH
from
	RAW_DATA.USER_SESSION_CHANNEL as US
join RAW_DATA.SESSION_TIMESTAMP as ST on
	US.SESSIONID = ST.SESSIONID;
~~~

- 세션의 수가 아닌 월별 액티브 유저를 카운트. 예를 들어 1번 유저가 11월에 10번 세션을 기록해도 1번으로 기록
-  year_month와 user_id로 distinct 적용

~~~sql
select
	distinct US.USERID,
	to_char(ST.TS, 'YYYY-MM') as YEAR_MONTH
from
	RAW_DATA.USER_SESSION_CHANNEL as US
join RAW_DATA.SESSION_TIMESTAMP as ST on
	US.SESSIONID = ST.SESSIONID
order by
	US.USERID;

~~~

~~~sql

select
	YEAR_MONTH,
	count(USERID) as CNT
from
	(
	select
		distinct US.USERID,
		to_char(ST.TS, 'YYYY-MM') as YEAR_MONTH
	from
		RAW_DATA.USER_SESSION_CHANNEL as US
	join RAW_DATA.SESSION_TIMESTAMP as ST on
		US.SESSIONID = ST.SESSIONID)
group by
	YEAR_MONTH
order by
	YEAR_MONTH ;
  ~~~
