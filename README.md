# OWASP ModSecurity Core Rule Set Plugin Registry
Registry for OWASP ModSecurity Core Rule Set plugins, official and 3rd party.

OWASP CRS allows for plugins. Yet the rule ID namespace needs to be coordinated. This repo serves as the official 
place to register plugins and reserve rule ID ranges.

The rule ID range from 9,500,000 - 9,999,999 is reserved for CRS plugins.

Plugins usually get a range of 1,000 IDs with the notable exception of the incubator plugin that
maps the regular CRS IDs from the 900K to the 9.9M range.


| *Plugin Name*              | *Rule ID Range*       | *Repository*                                                    | *Type*   |
|----------------------------|-----------------------|-----------------------------------------------------------------|----------|
| dummy                      | 9,500,000 - 9,500,999 | https://github.com/coreruleset/dummy-plugin                     | official |
| auto-decoding              | 9,501,000 - 9,501,999 | https://github.com/coreruleset/auto-decoding-plugin             | official |
| antivirus                  | 9,502,000 - 9,502,999 | https://github.com/coreruleset/antivirus-plugin                 | official |
| body-decompress            | 9,503,000 - 9,503,999 | https://github.com/coreruleset/body-decompress-plugin           | official |
| fake-bot                   | 9,504,000 - 9,504,999 | https://github.com/coreruleset/fake-bot-plugin                  | official |
| google-oauth2              | 9,505,000 - 9,505,999 | https://github.com/coreruleset/google-oauth2-plugin             | official |
| drupal-rule-exclusions     | 9,506,000 - 9,506,999 | https://github.com/coreruleset/drupal-rule-exclusions-plugin    | official |
| wordpress-rule-exclusions  | 9,507,000 - 9,507,999 | https://github.com/coreruleset/nextcloud-rule-exclusions-plugin | official |
| nextcloud-rule-exclusions  | 9,508,000 - 9,508,999 | TBC                                                             | official |
| dokuwiki-rule-exclusions   | 9,509,000 - 9,509,999 | TBC                                                             | official |
| cpanel-rule-exclusions     | 9,510,000 - 9,510,999 | TBC                                                             | official |
| xenforo-rule-exclusions    | 9,511,000 - 9,511,999 | TBC                                                             | official |
| phpbb-rule-exclusions      | 9,512,000 - 9,512,999 | https://github.com/coreruleset/phpbb-plugin                     | official |
| phpmyadmin-rule-exclusions | 9,513,000 - 9,513,999 | TBC                                                             | official |
| dos-protection             | 9,514,000 - 9,514,999 | TBC                                                             | official |
| incubator                  | 9,900,000 - 9,999,999 | https://github.com/coreruleset/incubator-plugin                 | official |
