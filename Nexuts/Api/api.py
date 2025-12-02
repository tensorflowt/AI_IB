from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from nexuts import InformationCenter
from Api.request_data import RegisterRequest, UpdateRequest, DeregisterRequest, SetStatus
from utils.utils import load_config
from utils.logger import logger


# 实例化信息中心（全局单例）
class APIServer:
    def __init__(self, args):
        self.args = args
        self.config = load_config(args.config_path)
        self.app = FastAPI(title="Information Center", version="1.0.0")
        self.info_center = InformationCenter(self.config)
        self._register_routes()

    def get_app(self):
        """返回 FastAPI 应用实例"""
        return self.app


    def _register_routes(self):
        """在此注册所有路由"""
        app = self.app

        @app.post("/v1/Nexuts/register")
        async def register_instance(request: RegisterRequest):
            """注册推理实例"""
            info = request.dict()
            result = self.info_center.register_instance(info)
            return result

        @app.post("/v1/Nexuts/set_status")
        async def set_status(request: SetStatus):
            info = request.dict()
            result = self.info_center.set_status(info)
            return result

        @app.post("/v1/Nexuts/deregister")
        async def delete_pod(request: DeregisterRequest):
            # TODO 删除实例
            info = request.dict()
            result = self.info_center.deregister_instance(info)
            return result

        @app.post("/v1/Nexuts/update_prefix_tree")
        async def update_prefix_tree(request: UpdateRequest):
            """接收 Sentry 节点上报的前缀树更新"""
            data = request.dict()
            logger.info("update prefix tree input:{}".format(data))

            result = self.info_center.update_prefix_tree(data)
            return JSONResponse(result)

        # @app.get("/instances")
        # async def list_instances():
        #     """查看当前注册的实例"""
        #     return JSONResponse(info_center.instances)

        @app.get("/v1/Nexuts/health")
        async def health_check():
            """简单健康检测"""
            return JSONResponse({"status": "ok"})

