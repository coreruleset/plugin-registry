# OWASP ModSecurity Core Rule Set Plugin Registry
Registry for OWASP ModSecurity Core Rule Set plugins, official and 3rd party.

OWASP CRS allows for plugins. Yet the rule ID namespace needs to be coordinated. This repo serves as the official 
place to register plugins and reserve rule ID ranges.

The rule ID range from 9,500,000 - 9,999,999 is reserved for CRS plugins.

Plugins usually get a range of 1,000 IDs with the notable exception of the incubator plugin that
maps the regular CRS IDs from the 900K to the 9.9M range.


| *Plugin Name*           | *Rule ID Range*       | *Repository*                                              | *Type*    |
|-------------------------|-----------------------|-----------------------------------------------------------|-----------|
| dummy                   | 9,500,000 - 9,500,999 | https://github.com/coreruleset/dummy-plugin               | official  |
| auto-decoding           | 9,501,000 - 9,501,999 | https://github.com/coreruleset/auto-decoding-plugin       | official  |
| antivirus               | 9,502,000 - 9,502,999 | https://github.com/coreruleset/antivirus-plugin           | official  |
| body-decompress         | 9,503,000 - 9,503,999 | https://github.com/coreruleset/body-decompress-plugin     | official  |
| fake-bot                | 9,504,000 - 9,504,999 | https://github.com/coreruleset/fake-bot-plugin            | official  |
| google-oauth2           | 9,505,000 - 9,505,999 | https://github.com/coreruleset/google-oauth2-plugin       | official  |
| pgadmin-rule-exclusions | 9,515,000 - 9,515,999 | https://github.com/flo-mic/pgadmin-rule-exclusions-plugin | 3rd party |
| incubator               | 9,900,000 - 9,999,999 | https://github.com/coreruleset/incubator-plugin           | official  |
