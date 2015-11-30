import settings
import importlib

router_path = 'routers.{0}'.format(settings.router)
router_class = importlib.import_module(router_path).Router

router = router_class(
    router_ip=settings.router_ip,
    router_port=settings.router_port,
    user=settings.user,
    password=settings.password,
)

logs = router.get_records()

for log in logs:
    print(log)