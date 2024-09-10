from acetylate_poc import schemas as poc_schemas

if __name__ == "__main__":

    import json
    from dataclasses import asdict

    metadata = poc_schemas.Metadata(
        authors=["John Doe"],
        descriptions=[
            poc_schemas.Description(
                title="Sample POC",
                content="This is a sample POC.",
                references=["https://example.com"]
            )
        ],
        cve=["CVE-2023-12345"],
        tags=["example", "security"]
    )

    target = poc_schemas.Target(
        type="network",
        network=poc_schemas.NetworkTarget(
            engine="Shodan",
            query="apache"
        )
    )

    payload = poc_schemas.Payload(
        type="http",
        http=poc_schemas.HttpPayload(
            data="GET / HTTP/1.1\r\nHost: example.com\r\n\r\n",
            headers={"User-Agent": "TestAgent"}
        )
    )

    assertions = [
        poc_schemas.Assertion(condition="status_code", value="200", message="Expected status code 200.")
    ]

    poc = poc_schemas.POCSchema(
        version="1.0",
        metadata=metadata,
        target=target,
        payload=payload,
        assertions=assertions
    )

    poc_dict = asdict(poc)
    poc_json = json.dumps(poc_dict, indent=4)
    print(poc_json)

    poc_dict = json.loads(poc_json)
    poc_instance = poc_schemas.POCSchema(
        version=poc_dict["version"],
        metadata=poc_schemas.Metadata(**poc_dict["metadata"]),
        target=poc_schemas.Target(**poc_dict["target"]),
        payload=poc_schemas.Payload(**poc_dict["payload"]),
        assertions=[poc_schemas.Assertion(**assertion) for assertion in poc_dict["assertions"]]
    )