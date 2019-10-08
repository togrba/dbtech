let $d:=doc("https://www.dbis.informatik.uni-goettingen.de/Mondial/mondial.xml")
<manycities>
let $qualcountries := (
for $qualcountry in $d/mondial/country
where count($country//city) > 40
return
    $qualcountry
)

for $country in $qualcountries
return if (count($country//city = 40))
    then <country name="{$country/name}">{count($country//city)}</country>
    else <country note="morethan60" name="{$country/name}">{count($country//city)}</country>
</manycities>
