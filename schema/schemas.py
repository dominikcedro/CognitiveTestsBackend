
# to deserialize singular
def individual_serial(evaluation) -> dict:
    return{
        "id": str(evaluation["_id"]),
        "type": str(evaluation["type"]),
        "description": str(evaluation["description"])
    }

# deserialaize multiple
def list_serial(evaluations)->list:
    return[individual_serial(evaluation) for evaluation in evaluations]

