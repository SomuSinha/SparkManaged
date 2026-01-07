with temp as 
(
select *, row_number() over (partition by ltrim(col1, '0'), ltrim(upc, '0') order by active_flag desc) as rnum
from tbl 
)
select * from temp where rnum=1



with temp as 
(
select * , row_number() over (partition by sku, upc order by date) rnum 
from tbl
),
temp2 as 
(
select * , max(rnum) over (partition by sku, upc) mx 
from temp
)
select * from temp2 where mx>1


--dense_rank for same rank to same value 1,2,2,3
--rank skips if same rank to 2 rows 1,2,2,4



with temp as 
(
select sku, upc
from tbl 
group by sku, upc
having count(distinct date) > 1


)
select t1.* from tbl t1
join temp t2 on ltrim(t1.sku, '0')=ltrim(t2.sku, '0') and t1.upc=t2.upc;



with temp as 
(
select sku, upc
from tbl 
group by sku, upc
having count(distinct date) > 1


)

select * from tbl where coalesce(sku, 'sku')|| coalesce(upc, 'upc') in (select coalesce(sku, 'sku')|| coalesce(upc, 'upc') from temp)


nullif(trim(col), '')

coalesce(trim(col), '')<>''


select 
from tbl1 t1 
left join 


select t1.*
from tbl1 t1
left join tbl2 t2 on t1.id = t2.id and t1.name = t2.name where t2.id is null


select t1.*, coalesce(first_value(tbl2.id) over (partition by id, name), 'test') fv
from tbl1 t1
left join tbl2 t2 on t1.id = t2.id and t1.name = t2.name where t2.id is null

--last_value

select * from stage 
union all 
select t.* from target t
left join stage s on t.id=s.id where s.id is null


--new not in old
select s.* from stage s
left join target t on s.id=t.id and s.name = t.name when t.id is null
union all 
--old not in new
select t.* from target t
left join stage s on t.id=s.id where s.id is null
union all
--common in both
select s.* from stage s
join target t on s.id=t.id and s.name = t.name
	

select coalesce(s.col1, t.col1), coalesce(s.col2, t.col2)
from stage1 s
full outer join target t on s.id = t.id and coalesce(s.name, 'name')=coalesce(t.name, 'name')



select s.* from stage s
join target t on s.id=t.id  
union all 
select t.* from target t
left join stage s on t.id=s.id where s.id is null



--full join as inner join 

insert overwrite into tbl 
select coalesce(s.col1, t.col1), coalesce(s.col2, t.col2)
from stage1 s
full outer join target t on s.id = t.id and coalesce(s.name, 'name')=coalesce(t.name, 'name') where (t.id is not null and s.id is not null) and (t.name is not null and s.name is not null)


delete from tbl 


insert into tbl 
select coalesce(s.col1, t.col1), coalesce(s.col2, t.col2)
from stage1 s
full outer join target t on s.id = t.id and coalesce(s.name, 'name')=coalesce(t.name, 'name') where (t.id is not null and s.id is not null) and (t.name is not null and s.name is not null)



select *, 
case when t2.id is null and t2.name is null then 'only in 2'
     when t2.id is null and t2.name is null then 'only in 2'
	 else 'null' end as result
from tbl1 t1 
full outer join tbl2 t2 on t1.id = t2.id and t1.name = t2.name 



select t1.*
from tbl1 t1
full outer join tbl2 t2 on t1.id = t2.id and t1.name = t2.name 
where (t2.id is null and t2.name is null ) or (t1.id is null and t1.name is null )


select t1.*
from tbl1 t1
full outer join tbl2 t2 on t1.id = t2.id and t1.name = t2.name 
where (t2.id is null and t2.name is null ) and (t1.id is null and t1.name is null )


with temp as 
(select id, cost::int-1 as cst from tbl)
select *, sum(cst) over (partition by id order by date)
from temp 

select max(marks) from tbl 

select id, max(marks) from tbl 
group by id 



select id, max(marks) mx from tbl 
group by id having max(marks) > 2

select id, name, count(*) as cnt
from tbl 
where name = 'test'
group by id, name 
having count(*) > 1


select id, 
max(marks) over (partition by id, name) mx,
count(marks) over (partition by id) cnt
from tbl 



select * from 
tbl where marks = (select min(marks) from tbl2)

select * from 
tbl where marks in (select marks from tbl2)



with temp as 
(select *, count(distinct uuid) over (partition by sku, upc) distinct_values
from tbl)
select * from temp where distinct_values > 1

delete from tbl where uuid in (select uuid from temp)


with temp as 
(select *, lead(start_date) over (partition by id order by start_date)
from tbl)


with temp as 
(select *, lead(start_date) over (partition by id order by name) ld 
from tbl)



with temp as 
(select *, lag(end_date) over (partition by id, name order by end_date)
from tbl)
update tbl 
set end_date = dateadd('day', -1, lad_start_date)
from temp where id=temp.id 


update tbl 
set col = case when col>2 then 1 else 0 end
from tbl 


update tbl
using 
(select * from tbl) k
set col = case when col>2 then 1 else 0 end
from tbl where tbl.id = k.id and sku in ()


with temp as (
select 
id, 
dense_rank() over (partition by id ) rnk1
dense_rank() over (partition by name) rnk2
)
select * from temp where rnk1 > 1 and rnk2 > 1


select dense_rank() over (partition by id, name order case when 'inisight' then 1 else 0 end) rnk 
from tbl 

--combine	
--union 
--union all 


--common 
--insersect

--difference
--except 
--minus 

select id, name from tbl
except 
select id, name from tbl2

--where property id is same but address changed
select t1.*
from tbl t1
join tbl2 t2 on t1.property_id = t2.property_id 
left join tbl2 t3 on t1.property_id = t3.property_id and t1.address = t3.address where t3.property_id is null and t3.address is null


select *, sum(marks) over (partition by id order by date)
from tbl 



select ss
from store_set_hierarachy ssh 
join store_set_member on ssh.id = ssm.parent_id  
join store_set_member on ssh.id = ssm.child_id

--reverse coalesce
temp.col =  coalesce(t5.col1, t4.col1, t3.col2, t2.col1, t1.col1) 


select * from tbll 
where employee in (select employee from tbl where designation='manager')


select e1.*
from employee e1  
join employee e2 on e1.id = e2.manager_id


with 
amazon_price as 
(select product_id, price 
from tbl where lower(company)='amazon'),
walmart_price as 
(select product_id, price 
from tbl where lower(company)='walmart')
select a.product_id, a.price as price_in_amazon, w.price as price_in_walmart
from amazon_price a 
full outer join walmart_price w on a.product_id = w.product_id




split(col, ' ')[0]
split_part(col, ',', 1)


soundex(a.col) = soundex (b.col)
jarowinkler_similarity(a.col) = jarowinkler_similarity(b.col)
substring(col, 1, 5)


test one 

select length(col) - length(replace(col, 't', ''))


reverse(split(reverse(url), '.')[0])


select left(col, 3)
select left(col, length(col)-1)


explode(split(col, ','))

to_date('12/12/2023', 'mm/dd/yyyy')
date_format('12/12/2023', 'mm/dd/yyyy')

with temp as 
(select id, date from new 
union all
select id, date from old),
temp2 as (
select id, dense_rank() over (partition by id order by date desc) rnk
from temp
)
select * from temp2 where rnk > 1


select *, row_number() over (partition by sku, upc order by case when active_flag=True then 1 else False end)
from tbl 


update product.product_set_member
set = case when sku>1 then 1 else 0 end
where product_set_member.id in (select id from tbl) and sku = upc


id 
1
2
7
8
9


with temp as 
(select *, lag(id) over (order by id) lg
from tbl )
select *, 
case when id-1=lg then 0 else id+1 end as missing_from , 
case when id-1=lg then 0 else lg-1 end as missing_till
from temp 


select col, listagg(col1, ', ')
from tbl 
group by col


select col, stringagg(col1, ', ')
from tbl 
group by col

select col, collect_set(name)
from tbl 
group by col

with temp as 
(
select explode(split(col, '#')) as tweets
from tbl 
)
select tweets, count(*)
from temp 
group by tweets


select id, to_json(struct(name, age)) as col 
from tbl 
group by id 



select to_json(map_from_enteries(array_construct(struct(name, age)))) over (partition by id)
from tbl 


concat(concat(col1, ','), 'col2')


concat_ws(',', col1, col2)


select charindex('/', col)


select substring(charindex('/', col)+12, length(col)-1)

select get_json_object(raw_data, '$.name')
select get_json_object(raw_data, '$.age')


current_date()


with temp as 
(select id , explode(split(col, ' ')) as word
from tbl )
select word, count(*) cnt 
from tbl 
group by word
order by cnt


execution order
---------------
from join 
where 
group by having 
select 
order by limit 


where before aggregation 
having after aggregation 


select id, sum(marks)
from tbl 
where id in (2, 4)
group by id
having sum(marks) > 2



select id, sum(marks) over (partition by id order by name)
from tbl 
where id in (2, 4)


alter table tbl 
rename column id to id_name 


alter table tbl 
add column col5 varchar col7 double; 

alter table tbl1
drop column col1, col2


create view xyz
select id, name from tbl 

delete from tbl 
truncate table tbl


select from tbl c where exists (select from tbl2 o where o.id=c.id)


Merge into tbl using 
(
select * from tbl

) stage 
on tbl.id=stage.id and tbl.name = stage.name 
when matched then update set tbl1.col1 = coalesce(stage.col1, stage.col2), tbl2.col2 = stage.col2 
when not matched then insert (tbl.id, tbl.name) values 
(stage.id, 
trim(stage.name)
)

--distinct 

regexp_replace('[A-Z]', '0')
regexp_like '[A-Z]'

like '%A%'
like 'B%'
replace('s', 0)

datediff('day', current_timestamp, current_timestamp-1)
dateadd('day', -1, current_timestamp())


select sum(case when id=2 then 1 else 0 end) as two_ids
from tbl 


select sum(case when id=2 then 1 else 0 end) as two_ids
from tbl
group by employee_name


select sum(case when id=2 then 1 else 0 end) over (partition by employee_name) as two_ids
from tbl


select dep, sum(case when occupancy_type='Residential' then 1 else 0 end) / count(*)
from tbl 
group by dep


select dep, sum(case when occupancy_type='Residential' then 1 else 0 end) over (partition by dep) / count(*) over (partition by dep)
from tbl 

--nullif(trim(col), '')

--coalesce(trim(col), '')=''


select dep, count(tbl2.name)
from tbl 
left join tbl2 on tbl.id = tbl2.id 
group by dep 



select dep, 100 * sum(case when occupancy_type='Residential' then 1 else 0 end) over (partition by dep) / count(*) over (partition by dep)
from tbl 


case when col1='test' then 1
     when (col1='test2' and col2='test3') then 0 
	 else 3 end
	 
	 
select tbl.*
from tbl 
join tbl2 on tbl.id = tbl2.id and tbl.name = tbl2.name 
where (
coalesce(nullif(trim(tbl.active_flag), '')), 'active_flag') <> coalesce(tbl2.active_flag, 'active_flag') or 
tbl.timestamp <> tbl2.timestamp
)


	 
select *,
case when tbl.active_flag <> tbl2.active_flag then 'active_flag_changed' 
     when tbl.timestamp <> tbl2.timestamp then 'timestamp_changed' 
as diff end
from tbl 
join tbl2 on tbl.id = tbl2.id and tbl.name = tbl2.name 
where (
coalesce(nullif(trim(tbl.active_flag), '')), 'active_flag') <> coalesce(tbl2.active_flag, 'active_flag') or 
tbl.timestamp <> tbl2.timestamp
)


update product.product_set_member
set 
sku = ltrim(sku, 0),
upc = ltrim(upc, 0)
where 
(product_set_member.sku <> stage.sku or 
product_set_member.upc <> stage.upc) and active_flag=True


