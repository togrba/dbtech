<mylist>
  {
  let $d:=doc("https://www.dbis.informatik.uni-goettingen.de/Mondial/mondial.xml")

  let $c:=$d/mondial/country
  let $result_list:=(
    for $country in $c
    let $city_data:=(
      for $city in $country//city
      let $alias_data:=(
        for $name in $city/name
        let $our_alias := ("&#x9;", "&#x9;", "&#x9;", <alias>{$name/text()}</alias>, "&#xA;")
        return $our_alias
      )
      return ("&#xA;", "&#x9;", "&#x9;", <city>{$city/@*[name() = "id"]}&#xA;{$alias_data}&#x9;&#x9;</city>)
    )
    let $country_name_tag := ("&#x9;", <country name="{$country/name}">{$city_data}&#xA;&#x9;</country>)
    return ("&#xA;", $country_name_tag)
  )
  return ($result_list, "&#xA;")
  }
</mylist>

(: Write output to file: xqilla d.xql > d_output.xml :)
