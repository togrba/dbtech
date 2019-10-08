let $mondial:=doc("https://www.dbis.informatik.uni-goettingen.de/Mondial/mondial.xml")
let $newdata := doc("newdata.xml")
<database>
    let $cities:=(
    for $city in $newdata/city
    return city/@name)

    let $olddata:=(
    for $oldinfo in $mondial/country//city
    where ($city/name in $cities)
    return ($city/name, $city/population))

    return (<city name="{data($city/@name/text())}"<data>
    <year>{$year}</year><people>{$population}</people>
    </data></city>)

</database>

(:
let $s1 := ('a', 'b')
let $s2 := ('a', 'c')
return ($s1, $s2) --> ('a','b','a','c')
:)