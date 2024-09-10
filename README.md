# acetylate-poc

## POC Schema

### `version`

- **Description**: Indicates the version of the POC file format. This helps in managing and validating schema compatibility.

### `metadata`

Provides additional context about the POC, including authorship, descriptions, CVE identifiers, and categorization tags.

- `authors` Array

  - **Description**: An array listing the authors of the POC, providing credit to those who developed or documented it.

- `descriptions` Array

  - **Description**: An array of descriptive sections providing context and details about the POC. Each description includes a title and content, with optional references.

    - **`title`**: A brief title summarizing the content of the description.
    - **`content`**: A detailed narrative explaining the POC, including its purpose, potential impact, and any relevant technical details.
    - **`references`** (Optional): An optional array of references supporting the description, such as links to reports, articles, or other documentation.

- `cve` (Optional)

  - **Description**: An optional array of CVE identifiers that relate the POC to specific known vulnerabilities.

- `tags` Array

  - **Description**: An array of tags used to categorize and provide searchable attributes for the POC.

### `target` (oneOf)

Specifies the target for the POC. The structure depends on the type of target.

- **`type`**: Specifies the type of target. For example, 'network' indicates the use of a network space search engine and query.
- **Additional Fields**: Depending on the `type`, additional fields such as `engine`, `query`, `port`, and `path` may be included.

### `payload` (oneOf)

Defines the payload used for the POC. The structure varies based on the payload type.

- **`type`**: The type of payload, such as 'http' or 'tcp', which determines the structure of the payload.
- **`data`**: The actual data or content of the payload to be sent to the target.
- **Additional Fields**: Based on the `type`, additional fields may include HTTP headers for 'http' payloads or custom data for 'tcp' payloads.

### `assertions` Array

A list of assertions to validate the POC's expected outcomes. Each assertion includes a condition to check and the expected value.

- **`condition`**: The type of condition to validate, such as 'status_code' or 'response_body_contains'.
- **`value`**: The expected result or condition to check for in the POC's response.
- **`message`** (Optional): An optional message to display if the assertion fails, providing context or details about the failure.