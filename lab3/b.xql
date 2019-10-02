let $d:=doc("https://www.dbis.informatik.uni-goettingen.de/Mondial/mondial.xml")
return $d/mondial/mountain[matches(mountains, 'Hawaii') and (@type='volcano')]/name
