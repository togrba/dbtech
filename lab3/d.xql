let $d:=doc("https://www.dbis.informatik.uni-goettingen.de/Mondial/mondial.xml")
let $d_output:=doc("file:///Users/Bang/code/dbtech/lab3/d_output.xml")/mylist/*

let $c := $d/mondial/country

let $result_list := (

    for $country in $c

    let $city_data := (
      for $city in $country//city

      let $alias_data := (
        for $name in $city/name
        return ("&#xA;", <alias>{$name/text()}</alias>)

      )
      return ("&#xA;", <city>{$city/@*[name() = "id"]}{$alias_data}&#xA;</city>)

    )
    let $country_name_tag := (<country name="{$country/name}">{$city_data}&#xA;</country>)
    return ("&#xA;", $country_name_tag)

)
return (<mylist>{$result_list}&#xA;</mylist>, $d_output)


(: Write output to file: xqilla d.xql > d_output.xml :)
