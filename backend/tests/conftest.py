import pytest
from user.models import User
from django.test.client import Client


class ClientWithJsonDefault(Client):
    """
    魔改 Django 自带的 Test Client 使其默认请求类型为 json
    肯定还有更优雅的实现方式
    """
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs, content_type='application/json')

    def options(self, *args, **kwargs):
        return super().options(*args, **kwargs, content_type='application/json')

    def put(self, *args, **kwargs):
        return super().put(*args, **kwargs, content_type='application/json')

    def patch(self, *args, **kwargs):
        return super().patch(*args, **kwargs, content_type='application/json')

    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs, content_type='application/json')


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


# 大部分是直接抄库的
# TODO 感觉应该有别的方法
@pytest.fixture(scope="session")
def django_db_setup(
    request,
    django_test_environment,
    django_db_blocker,
    django_db_use_migrations,
    django_db_keepdb,
    django_db_createdb,
    django_db_modify_db_settings,
):
    """Top level fixture to ensure test databases are available"""
    from django.test.utils import setup_databases, teardown_databases

    setup_databases_args = {}

    if django_db_keepdb and not django_db_createdb:
        setup_databases_args["keepdb"] = True

    with django_db_blocker.unblock():
        db_cfg = setup_databases(
            verbosity=request.config.option.verbose,
            interactive=False,
            **setup_databases_args
        )

        # 初始化时添加用户
        User.objects.create(username="test", nickname="test_nickname",
                            password='test')
        User.objects.create(username="test2", nickname="test_nickname2",
                            password='test')

    def teardown_database():
        with django_db_blocker.unblock():
            try:
                teardown_databases(db_cfg, verbosity=request.config.option.verbose)
            except Exception as exc:
                request.node.warn(
                    pytest.PytestWarning(
                        "Error when trying to teardown test databases: %r" % exc
                    )
                )

    if not django_db_keepdb:
        request.addfinalizer(teardown_database)


@pytest.fixture(scope='function')
def user():
    # user = User.objects.create(username="test", nickname="test_nickname",
    #                            password='test')
    user = User.objects.get(username="test")
    return user


@pytest.fixture(scope='function')
def c():
    client = ClientWithJsonDefault()
    client.login(username='test', password='test')
    return client
