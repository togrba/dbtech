let $d:=doc("https://www.dbis.informatik.uni-goettingen.de/Mondial/mondial.xml")
let $newdata := doc("newdata.xml")

let $cities:=(
for $city in $newdata/database/city
return data($city/@name)
)					(: ger Stockholm och New York på varsin rad :)

let $olddata:=(
for $cit in $cities
	for $city in $d/mondial/country//city	(: ger gammal info om Stockholm och New York :)
	where $city/name = $cit
	return ($city/name, "&#xA;", $city/population)
)

return (<database>&#xA;{$olddata}&#xA;</database>)

(: return (<city name="{data($city/@name/text())}"<data>
<year>{$year}</year><people>{$population}</people>
</data></city>)

let $result:=(
for $city in $cities
	return
	<city name="{$city/name}">
	<data><year>{$city/year}</year><people>{$city/people}</people></city>
)


:)
(:
return
<database>
$result
</database> :)

(:
let $s1 := ('a', 'b')
let $s2 := ('a', 'c')
return ($s1, $s2) --> ('a','b','a','c')
:)
