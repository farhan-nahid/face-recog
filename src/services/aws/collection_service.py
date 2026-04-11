from .client import rekognition_client
from .decorators import aws_safe


@aws_safe
def create_collection(collection_name: str):
    """
    Create a new collection in AWS Rekognition.

    Args:
        collection_name: The name of the collection to create.

    Returns:
        dict: Response containing collection details.
    """
    response = rekognition_client.create_collection(CollectionId=collection_name)
    return {
        "data": {
            "collection_arn": response.get("CollectionArn"),
            "face_model_version": response.get("FaceModelVersion"),
            "status_code": response.get("StatusCode"),
        }
    }


@aws_safe
def get_all_collections():
    """
    Retrieve all collections from AWS Rekognition.

    Returns:
        dict: Response containing list of all collections.
    """
    response = rekognition_client.list_collections()
    return {
        "data": {
            "collections": response.get("CollectionIds", []),
            "face_model_versions": response.get("FaceModelVersions", []),
        }
    }


@aws_safe
def get_collection(collection_name: str):
    """
    Retrieve a specific collection from AWS Rekognition.

    Args:
        collection_name: The name of the collection to retrieve.

    Returns:
        dict: Response containing collection details.
    """
    response = rekognition_client.describe_collection(CollectionId=collection_name)
    return {
        "data": {
            "collection_arn": response.get("CollectionArn"),
            "face_count": response.get("FaceCount"),
            "face_model_version": response.get("FaceModelVersion"),
            "created_timestamp": str(response.get("CreationTimestamp")),
        }
    }


@aws_safe
def delete_collection(collection_name: str):
    """
    Delete a collection from AWS Rekognition.

    Args:
        collection_name: The name of the collection to delete.

    Returns:
        dict: Response containing deletion status.
    """
    response = rekognition_client.delete_collection(CollectionId=collection_name)
    return {
        "data": {
            "status_code": response.get("StatusCode"),
        }
    }
