from gym.envs.registration import register

register(
    id='chrome-trex-v0',
    entry_point='chrome_trex_gym.envs:ChromeTrexEnv',
)