let $d:=doc("https://www.dbis.informatik.uni-goettingen.de/Mondial/mondial.xml")
let $newdata:=doc("newdata.xml")

let $our_cities:=(
	for $city in $newdata/database/city
	return data($city/@name)					(: outputs Stockholm New York :)
)

let $newdata_list:=(
	for $allnew in $newdata/database/*
	return $allnew						(: outputs original newdata :)
)

let $olddata:=(
	for $cit in $our_cities
	for $city in $d/mondial/country//city			(: outputs old Stockholm and New York info in newdata format:)
		where $city/name = $cit
		let $data := (
			let $our_pops := $city/population
			let $our_years := (
					for $year_data in $our_pops
					let $year := <year>{data($year_data/@year)}</year>
					let $year_pop := <people>{$year_data[@year]/text()}</people>
					order by $year descending
					return (<data>&#xA;    {$year}&#xA;    {$year_pop}&#xA;</data>, "&#xA;")
			)
			return $our_years
		)
		let $our_city := <city name="{$city/name}">&#xa;{$data}</city>
		return $our_city
)

(:
let $hey:=(
for $s1 in $newdata_list
where $s1//@name = "Stockholm"   	(: GER RÄTT INFO FRÅN NEWDATA DÄR CITY NAME = STOCKHOLM :)
return $s1//data
)
return $hey
:)


(:										(:FUNKAR FÖR SPECIFICERAD STAD, SER RÄTT UT:)
let $oldsort:=(for $y in $olddata where $y//@name = "Stockholm" return $y/*)
let $sorteddata:=(for $x in $newdata_list where $x//@name = "Stockholm" return <city name="{$x//@name}">&#xa;{$x/*}{$oldsort}&#xa;</city>)
return $sorteddata
:)


(:
let $result:=(									(: DET VI VILL HA UTAN HÅRDKODNING, FUNKAR EJ :)
	let $c:=(for $city in $our_cities return $city)
		let $oldsort:=(for $y in $olddata where $y//@name = "{data($c)}" return $y/*)
		let $sorteddata:=(for $x in $newdata_list where $x//@name = "{data($c)}" return <city name="{$x//@name}">&#xa;{$x/*}{$oldsort}&#xa;</city>)
	return $sorteddata
)
return $result :)

let $oldsto:=(for $y in $olddata where $y//@name = "Stockholm" return $y/*)
let $sortedsto:=(for $x in $newdata_list where $x//@name = "Stockholm" return <city name="{$x//@name}">&#xa;{$x/*}{$oldsto}&#xa;</city>)
let $oldny:=(for $y in $olddata where $y//@name = "New York" return $y/*)
let $sortedny:=(for $x in $newdata_list where $x//@name = "New York" return <city name="{$x//@name}">&#xa;{$x/*}{$oldny}&#xa;</city>)
return ($sortedsto,$sortedny)
