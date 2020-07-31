## 2주차 과제

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

- 월별 userid개수를 count
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

## 가상의 데이터 인프라 구축하기

- 어떤 데이터들을 데이터 웨어하우스로 복사해오고 싶은지(raw_data로 들어갈 데이터들)

- 어떤 형태의 summary table들을 만들고 싶은지 (analytics폴더 밑에 만들어질 테이블들)

- KT IPTV 데이터를 접해본 경험이 있습니다. 이를 바탕으로 raw_data및 summary_table을 구성해보았습니다.

- 유저, 컨텐츠, 플랫폼(OTV, OTM) 크게 3가지로 구분할 수 있습니다. 



![](https://user-images.githubusercontent.com/36406676/89041604-9fe3c300-d380-11ea-8e39-0d019009a8f4.png)
