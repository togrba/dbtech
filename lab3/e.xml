let $d:=doc("https://www.dbis.informatik.uni-goettingen.de/Mondial/mondial.xml")

let $qualcountries:=(
    for $qualcountry in $d/mondial/country
    where count($qualcountry//city) > 40
    return
        $qualcountry
)

let $result:=(
    for $country in $qualcountries
    return if (count($country//city) < 60)
        then <country name="{$country/name}">{count($country//city)}</country>
        else <country note="morethan60" name="{$country/name}">{count($country//city)}</country>
)

return
    <manycities>
        {$result}
    </manycities>
