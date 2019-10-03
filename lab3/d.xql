let $d:=doc("https://www.dbis.informatik.uni-goettingen.de/Mondial/mondial.xml")
(:
for $data in $d/mondial/country/name
return
    <mylist>
        {$data}
    </mylist>
GER:
<mylist><name>Albania</name></mylist>
<mylist><name>Greece</name></mylist>
....DVS ländernas namn


for $data in $d/mondial/country/city[(@id)]/name
return
    <mylist>
        {$data}
    </mylist>
GER:
<mylist><name>Tirana</name></mylist>
<mylist><name>Tirane</name></mylist>
<mylist><name>Shkodër</name></mylist>
.... DVS städernas olika alias


for $dataid in $d/mondial/country/city
return
    <mylist>
    {data($dataid/@id)}
    </mylist>
GER:
<mylist>cty-Albania-Tirane</mylist>
<mylist>stadt-Shkoder-AL-AL</mylist>
....DVS city id
:)