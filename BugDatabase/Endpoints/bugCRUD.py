from flask import request, make_response, jsonify
from gateway import bugGateway

# TODO : put return codes at top without the jsonify method



def create_bug():
    """
    Greate a bug and but it into the database
    :return:
    """
    if request.method == 'POST':

        code400 = make_response(jsonify([{"message": "bug name is not between 1 and 100 characters"},
                                         {"message": "description is not between 1 and 500 characters"},
                                         {"message": "priority not between 1 and 4"}]), 400)

        # Get the necessary data from the post request (if it exists)
        name = request.form.get('name')
        description = request.form.get('description')
        priority = request.form.get('priority')

        # Checks to see if the given data meets the requirements
        if not (name and description and priority):
            return code400
        if len(name) >= 100 or len(description) >= 500 or 1 > int(priority) or int(priority) > 4:
            return code400

        # If all checks have passed, attempt to make a new bug
        # The object itself should attempt to put the data into the database
        # Once the object is created, it should return a message with the id of the newly created object
        bug_id = bugGateway.create_bug(name, description, priority)
        response = make_response(jsonify({"message": "added", "id": bug_id}), 200)
        return response


def get_bugs():
    """
    Get all available bugs currently in the database
    :return: A list of all stored bugs and their details
    """

    if request.method == 'GET':
        # reach out to database to get information
        bugs = bugGateway.get_bugs()

        print(bugs)

        # return list of bugs
        bugs = [{"id": int(bug[0]),
                 "name": bug[1].decode(),
                 "description": bug[2].decode(),
                 "priority": bug[3]} for bug in bugs]

        response = make_response(jsonify(bugs), 200)
        return response


def delete_bug(id):
    """
    Delete a specified bug
    :param id: Id given to the bug upon creation
    :return: A message saying the bug was deleted
    """

    if request.method == 'DELETE':

        # Test to see if the given value is really an integer
        try:
            id = int(id)
        except ValueError:
            return make_response('{"message": "Incorrect bug Id"}', 400)

        # Delete the bug using the given id
        bug = bugGateway.delete_a_bug(id)

        # If no id was returned, respond with an error message
        if bug == 0:
            return make_response('{"message": "Bug could not be found"}', 404)

        return make_response(jsonify({"message": "Deleted"}), 200)


def update_bug(id):

    if request.method == 'PUT':
        code404 = make_response(jsonify({"message": "Bug could not be found"}), 404)

        code400 = make_response(jsonify([{"message": "Bug name is not between 1 and 100 characters"},
                                         {"message": "Description is not between 1 and 500 characters"},
                                         {"message": "Priority not between 1 and 4"}]), 400)

        code400ID = make_response(jsonify({"message": "Incorrect Bug Id"}), 400)

        code200 = make_response(jsonify({"message": "Updated"}), 200)

        # Test if the given ID is really an integer
        try:
            int(id)
        except ValueError:
            return code400ID

        # Get original data from the bug being updated
        original_bug = bugGateway.get_a_bug(id)

        # If the selected bug doesn't exist, return a 404 (not found)
        if original_bug == 0:
            return code404

        # Get data from request if it exists
        updated_bug = []

        updated_bug.append(request.form.get('name'))
        updated_bug.append(request.form.get('description'))
        updated_bug.append(request.form.get('priority'))

        # If any values from the request are not included (or are left empty), replace them with the original value.
        k = 0
        for i in range(3):
            if not updated_bug[i]:
                updated_bug[i] = original_bug[i + 1]
                k += 1
        if k == 3:
            return code400  # Returns a response code for incorrect data 400

        if len(updated_bug[0]) >= 100 or len(updated_bug[1]) >= 500:  # Checks to see if the minimum requirements are met
            print(updated_bug)
            return code400

        # If everything is correct, update the bug in the database
        bug = bugGateway.update_bug(updated_bug[0],     # Name
                                       updated_bug[1],  # Description
                                       updated_bug[2],  # Priority
                                       int(id))

        return code200