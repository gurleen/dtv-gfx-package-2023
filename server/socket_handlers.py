from app import sio
from enum import Enum, auto
from loguru import logger
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
from pydantic import BaseModel

from templates.template import Template
from rosters import get_team_by_id, get_roster_for_team


executor = ThreadPoolExecutor(max_workers=3)


class RendererState(Enum):
    NotPlaying = auto()
    InAnimation = auto()
    Playing = auto()
    MiddleAnimation = auto()
    OutAnimation = auto()


class TeamsInfo(BaseModel):
    home_id: int
    away_id: int
    sport: str


class Renderer:
    state: RendererState
    graphic: Template
    global_data: list[dict]
    teams_info: TeamsInfo

    def __init__(self):
        self.state = RendererState.NotPlaying
        self.graphic = None
        self.global_data = list()
        self.teams_info = TeamsInfo(home_id=2182, away_id=232, sport="womens")

    def get_state(self) -> dict:
        return dict(state=self.state.name, id=self.graphic.id if self.graphic else None, name=self.graphic.name if self.graphic else None)

    async def set_state(self, state: RendererState):
        self.state = state
        await sio.emit("rendererState", self.get_state())
        logger.info(f"Renderer state set to {state.name}")

    async def play(self, graphic: Template) -> bool:
        if self.state == RendererState.NotPlaying:
            # self.data.update(graphic.vars)
            payload = {**graphic.model_dump(), "global": self.global_data}
            await sio.emit("rendererPlay", json.dumps(payload))
            await sio.emit("currentAnimationId", graphic.id)
            await self.set_state(RendererState.InAnimation)
            self.graphic = graphic
            return True
        return False

    async def running(self) -> bool:
        if self.state in [RendererState.InAnimation, RendererState.MiddleAnimation, RendererState.OutAnimation]:
            await self.set_state(RendererState.Playing)
            return True
        return False

    async def stop(self) -> bool:
        if self.state == RendererState.Playing:
            await sio.emit("rendererStop")
            await self.set_state(RendererState.OutAnimation)
            return True
        return False

    async def stopped(self) -> bool:
        if self.state in [RendererState.OutAnimation, RendererState.MiddleAnimation]:
            renderer.graphic = None
            await self.set_state(RendererState.NotPlaying)
            return True
        return False
    
    async def blank(self) -> bool:
        await sio.emit("rendererBlank")
        self.graphic = None
        await self.set_state(RendererState.NotPlaying)
        return True
    
    async def next(self) -> bool:
        if self.state == RendererState.Playing:
            await sio.emit("rendererNext")
            await self.set_state(RendererState.MiddleAnimation)
            return True
        return False
    
    async def update_global_var(self, key: str, value: str):
        logger.info(f"Updated global var {key} to {value}")
        self.global_data.append(dict(key=key, value=value))
        await sio.emit("globalVarUpdated", key, value)


renderer = Renderer()


@sio.on("requestRendererPlay")
async def request_renderer_play(sid: str, graphic_json: dict):
    graphic = Template(**graphic_json)
    logger.info(f"{sid} requested to play {graphic} with data {graphic.vars}")
    return await renderer.play(graphic)

@sio.on("requestRendererStop")
async def request_renderer_stop(sid: str):
    logger.info(f"{sid} requested to stop")
    return await renderer.stop()

@sio.on("requestRendererBlank")
async def request_renderer_blank(sid: str):
    logger.info(f"{sid} requested to blank")
    return await renderer.blank()

@sio.on("requestRendererNext")
async def request_renderer_next(sid: str):
    logger.info(f"{sid} requested to next")
    return await renderer.next()

@sio.on("setRendererRunning")
async def set_renderer_running(sid: str):
    logger.info(f"{sid} set renderer to running")
    return await renderer.running()

@sio.on("setRendererStopped")
async def set_renderer_stopped(sid: str):
    logger.info(f"{sid} set renderer to stopped")
    return await renderer.stopped()

@sio.on("requestRendererState")
async def request_renderer_state(sid: str):
    logger.info(f"{sid} requested renderer state")
    return renderer.get_state()

@sio.on("updateGraphicVars")
async def update_graphic_vars(sid: str, vars: dict):
    logger.info(f"{sid} updated graphic vars to {vars}")
    renderer.graphic.vars = vars
    await sio.emit("graphicVarsUpdated", renderer.graphic.vars)

@sio.on("updateGlobalVar")
async def updated_global_var(sid: str, key: str, value: str):
    await renderer.update_global_var(key, value)

@sio.on("getGlobalVars")
async def get_global_vars(sid: str):
    logger.info(f"{sid} requested global vars")
    return renderer.global_data

@sio.on("setTeams")
async def set_teams(sid: str, home_id: int, away_id: int, sport: str):
    logger.info(f"{sid} set teams to {home_id} and {away_id}")
    renderer.teams_info = TeamsInfo(home_id=home_id, away_id=away_id, sport=sport)
    home = get_team_by_id(home_id)
    away = get_team_by_id(away_id)
    await renderer.update_global_var("Home-ID", home_id)
    await renderer.update_global_var("Away-ID", away_id)
    await renderer.update_global_var("Sport", sport)
    await renderer.update_global_var("Home-Name", home.short_name)
    await renderer.update_global_var("Home-Abbr", home.abbreviation)
    await renderer.update_global_var("Home-Full-Name", home.display_name)
    await renderer.update_global_var("Home-School-Name", home.team)
    await renderer.update_global_var("Home-Team-Name", home.mascot)
    await renderer.update_global_var("img:Home-Logo", home.white_logo)
    await renderer.update_global_var("Away-Name", away.short_name)
    await renderer.update_global_var("Away-Abbr", away.abbreviation)
    await renderer.update_global_var("Away-Full-Name", away.display_name)
    await renderer.update_global_var("Away-School-Name", away.team)
    await renderer.update_global_var("Away-Team-Name", away.mascot)
    await renderer.update_global_var("img:Away-Logo", away.white_logo)
    await renderer.update_global_var("color:Home-Color", "#" + home.color)
    await renderer.update_global_var("color:Away-Color", "#" + away.color)
    sport_code = "wbb" if sport == "womens" else "mbb"
    await renderer.update_global_var("Home-Roster-Dir", f"{home.abbreviation.lower()}-{sport_code}")
    await renderer.update_global_var("Away-Roster-Dir", f"{away.abbreviation.lower()}-{sport_code}")

    loop = asyncio.get_running_loop()
    loop.run_in_executor(executor, get_roster_for_team, sport, home_id)
    loop.run_in_executor(executor, get_roster_for_team, sport, away_id)

@sio.on("getTeams")
async def get_teams(sid: str):
    logger.info(f"{sid} requested teams")
    return renderer.teams_info.dict()