# OWASP ModSecurity Core Rule Set Plugin Registry
Registry for OWASP ModSecurity Core Rule Set plugins, official and 3rd party.

OWASP CRS allows for plugins. Yet the rule ID namespace needs to be coordinated. This repo serves as the official 
place to register plugins and reserve rule ID ranges.

The rule ID range from 9,500,000 - 9,999,999 is reserved for CRS plugins.

Plugins usually get a range of 1,000 IDs with the notable exception of the incubator plugin that
maps the regular CRS IDs from the 900K to the 9.9M range.


| *Plugin Name* | *Rule ID Range*     | *Website* |
|---------------|---------------------|-----------|
| dummy         | 9,500,000 - 9,500,999 | https://github.com/coreruleset/dummy-plugin |
| auto-decoding | 9,501,000 - 9,501,999 | https://github.com/coreruleset/auto-decoding-plugin |
| incubator     | 9,900,000 - 9,999,999 | https://github.com/coreruleset/incubator-plugin |
