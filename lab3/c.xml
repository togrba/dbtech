let $d:=doc("https://www.dbis.informatik.uni-goettingen.de/Mondial/mondial.xml")
for $m in $d/mondial/mountain
where $m/elevation > 8000
order by $m/elevation
return <bigmountain><height>{data($m/elevation)} meters</height>{($m/name)}</bigmountain>
