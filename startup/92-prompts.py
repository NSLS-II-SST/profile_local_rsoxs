run_report(__file__)

from IPython.terminal.prompts import Prompts, Token
from datetime import datetime


class RSoXSPrompt(Prompts):
    def in_prompt_tokens(self, cli=None):
        dt = datetime.now()
        formatted_date = dt.strftime('%Y-%m-%d')

        if len(RE.md['user_name']) > 0 and len(RE.md['project_name']) > 0 and len(RE.md['institution']) > 0:
            RSoXStoken = (Token.Prompt, 'RSoXS {}/{}/{}/{} '.format(RE.md['institution'],
                                                                    RE.md['user_name'],
                                                                    RE.md['project_name'],
                                                                    formatted_date))
        else:
            RSoXStoken = (Token.OutPrompt, 'RSoXS (define metadata before scanning)')
        return [RSoXStoken,
                (Token.Prompt, ' ['),
                (Token.PromptNum, str(self.shell.execution_count)),
                (Token.Prompt, ']: ')]

ip = get_ipython()
ip.prompts = RSoXSPrompt(ip)


def beamline_status():
    # user()
    sample()
    boxed_text('Detector status',
               exposure()+'\n'+sw_det.binning()+'\n'+sw_det.cooling_state(),
               'lightblue',80,shrink=True)

user()
beamline_status()