let $d:=doc("https://www.dbis.informatik.uni-goettingen.de/Mondial/mondial.xml")
    <mylist>
for $country in $d/mondial/country
return
        <country name="{$country/name}">
        let $cityids:=$d/mondial/country/city
        for $cityid in $cityids
        return
            <city id="{data($cityid/@id/text())}">
                let $aka:=$d/mondial/country/city[(@id)]/name
                for $alias in $aka
                return
                    <alias>
                        {$alias/text()}
                    </alias>
            </city>
        </country>
    </mylist>

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


for $cityid in $d/mondial/country/city
return
    <mylist>
    {data($cityid/@id)}
    </mylist>
GER:
<mylist>cty-Albania-Tirane</mylist>
<mylist>stadt-Shkoder-AL-AL</mylist>
....DVS city id



<country name="{$country/name}">
GER:
<country name ="Albania">
<country name ="Greece">
.... {} returns values, without these - the expression/query itself is returned as a string
:)