let $d:=doc("https://www.dbis.informatik.uni-goettingen.de/Mondial/mondial.xml")
let $newdata:=doc("newdata.xml")

let $our_cities:=(
	for $city in $newdata/database/city
	return data($city/@name)					(: output: Stockholm New York :)
)

let $newdata_list:=(
	for $all in $newdata/database/city
	return $all						(: output: original newdata :)
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

let $output_data:=(
	for $city in $our_cities
	let $combined_data:=($newdata_list, $olddata)
	for $output in $combined_data
	where $city = data($output/@name)
		for $data in $output
		return ($data, "&#xA;")
)

return (<database>&#xA;{$real}</database>)

(: Write output to file: xqilla f.xql > f_output.xml :)
