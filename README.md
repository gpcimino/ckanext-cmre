ckanext-cmre
============

Available plugins:

- `cmre_harvester`: a file system harvester for ISO documents; will parse some EKOE specific fields
- `cmre_facets`: will handle some EKOE specific fields as facets


Configuration
-------------

Install the extension:
```
pip install -e .
```

In order to handle the facets properly, you'll have to add edit the Solr configuration, adding these fields:
```
<field name="ekoe_platform"   type="string" indexed="true" stored="true" multiValued="true"/>
<field name="ekoe_cruise"     type="string" indexed="true" stored="true" multiValued="true"/>
<field name="ekoe_instrument" type="string" indexed="true" stored="true" multiValued="true"/>
<field name="ekoe_owner"      type="string" indexed="true" stored="true" multiValued="true"/>
```
