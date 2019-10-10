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
		for $city in $d/mondial/country//city					(: ger gammal info om Stockholm och New York :)
		where $city/name = $cit
		let $data := (
			let $our_pops := $city/population
			let $our_years := (
					for $year_data in $our_pops
					let $year := ("&#x20;", "&#x20;", "&#x20;", <year>{data($year_data/@year)}</year>)
					let $year_pop := ("&#x20;", "&#x20;", "&#x20;", <people>{$year_data[@year]/text()}</people>)
					order by data($year_data/@year) descending
					return (<data>&#xA;{$year}&#xA;{$year_pop}&#xA;</data>, "&#xA;")
			)
			return $our_years
		)
		let $our_city := <city name="{$city/name}">&#xa;{$data}</city>
		return $our_city
)


let $oldsto:=(
	for $y in $olddata
	where $y//@name = "Stockholm"
	return $y/*
)
let $sortedsto:=(
	for $x in $newdata_list
	where $x//@name = "Stockholm"
	return <city name="{$x//@name}">&#xa;{$x/*}{$oldsto}&#xa;</city>
)
let $oldny:=(
	for $y in $olddata
	where $y//@name = "New York"
	return $y/*
)
let $sortedny:=(
	for $x in $newdata_list
	where $x//@name = "New York"
	return <city name="{$x//@name}">&#xa;{$x/*}{$oldny}&#xa;</city>
)
return ($sortedsto,$sortedny)
