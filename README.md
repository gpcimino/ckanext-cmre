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
<field name="ekoe_trial"           type="string" indexed="true" stored="true" multiValued="true"/>
<field name="ekoe_platform"        type="string" indexed="true" stored="true" multiValued="true"/>
<field name="ekoe_sensor"          type="string" indexed="true" stored="true" multiValued="true"/>
<field name="ekoe_experiment"      type="string" indexed="true" stored="true" multiValued="true"/>
<field name="ekoe_owner_org"       type="string" indexed="true" stored="true" multiValued="false"/>
<field name="ekoe_dimension"       type="string" indexed="true" stored="true" multiValued="true"/>
<field name="ekoe_classification"  type="string" indexed="true" stored="true" multiValued="true"/>
<field name="ekoe_identifier"      type="string" indexed="true" stored="true" multiValued="true"/>
```
