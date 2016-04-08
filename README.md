# PoliticalContributions

### Table Schemas

#### Contributions

| Column Name		| Data Type	|
| ----------------------|:-------------:|
| committee_id		| string	|
| candidate_id		| string	|
| candidate_name	| string	|
| contributor_name	| string	|
| contributor_city	| string	|
| contributor_state	| string	|
| contributor_zip	| int		|
| contributor_employer	| string	|
| contributor_occupation| string	|
| contribution_amount	| int		|
| contribution_date	| string	|
| receipt_description	| string	|
| memo_code		| string	|
| memo_text		| string	|
| form_type		| string	|
| report_number		| int		|
| transaction_id	| string	|
| election_type		| string	|

More info at ftp://ftp.fec.gov/FEC/Presidential_Map/2016/DATA_DICTIONARIES/CONTRIBUTOR_FORMAT.txt

#### Expenditures

| Column Name			| Data Type	|
| ------------------------------|:-------------:|
| committee_id			| string	|
| candidate_id			| string	|
| candidate_name		| string	|
| recipient_name		| string	|
| disbursement_amonut		| int		|
| disbursement_date		| string	|
| recipient_city		| string	|
| recipient_state		| string	|
| recipient_zip			| int		|
| disbursement_description	| string	|
| memo_code			| string	|
| memo_text			| string	|
| form_type			| string	|
| report_number			| int		|
| transaction_id		| string	|
| election_type			| string	|

More info at ftp://ftp.fec.gov/FEC/Presidential_Map/2016/DATA_DICTIONARIES/EXPENDITURE_FORMAT.txt

#### Candidates

| Column Name	| Data Type	|
| --------------|:-------------:|
| id		| string	|
| name		| string	|
| election_type	| string	|
| party		| string	|
