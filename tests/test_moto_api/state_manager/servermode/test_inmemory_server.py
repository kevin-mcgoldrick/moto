import json
import sure  # noqa # pylint: disable=unused-import


from moto import server


def test_set_transition():
    backend = server.create_backend_app("moto_api")
    test_client = backend.test_client()

    post_body = dict(
        model_name="server::test1",
        transition={"progression": "waiter", "wait_times": 3},
    )
    resp = test_client.post(
        "http://localhost:5000/moto-api/state-manager/set-transition",
        data=json.dumps(post_body),
    )
    resp.status_code.should.equal(201)

    resp = test_client.get(
        "http://localhost:5000/moto-api/state-manager/get-transition?model_name=server::test1"
    )
    resp.status_code.should.equal(200)
    json.loads(resp.data).should.equal({"progression": "waiter", "wait_times": 3})


def test_unset_transition():
    backend = server.create_backend_app("moto_api")
    test_client = backend.test_client()

    post_body = dict(
        model_name="server::test2",
        transition={"progression": "waiter", "wait_times": 3},
    )
    test_client.post(
        "http://localhost:5000/moto-api/state-manager/set-transition",
        data=json.dumps(post_body),
    )

    post_body = dict(model_name="server::test2")
    resp = test_client.post(
        "http://localhost:5000/moto-api/state-manager/unset-transition",
        data=json.dumps(post_body),
    )
    resp.status_code.should.equal(201)

    resp = test_client.get(
        "http://localhost:5000/moto-api/state-manager/get-transition?model_name=server::test2"
    )
    resp.status_code.should.equal(200)
    json.loads(resp.data).should.equal({"progression": "immediate"})


def test_get_default_transition():
    backend = server.create_backend_app("moto_api")
    test_client = backend.test_client()

    resp = test_client.get(
        "http://localhost:5000/moto-api/state-manager/get-transition?model_name=unknown"
    )
    resp.status_code.should.equal(200)
    json.loads(resp.data).should.equal({"progression": "immediate"})
