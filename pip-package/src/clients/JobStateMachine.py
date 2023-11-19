from statemachine import StateMachine, State


class JobStateMachine(StateMachine):
    started = State(initial=True)
    downloading_base_image = State()
    installing_user_pip_dependencies = State()
    image_built = State()
    pushing_image = State()
    image_pushed = State(final=True)

    base_image_not_found = started.to(downloading_base_image)
    base_image_downloaded = downloading_base_image.to(installing_user_pip_dependencies)
    base_image_found = started.to(installing_user_pip_dependencies)
    user_pip_dependencies_installed = installing_user_pip_dependencies.to(image_built)
    image_built = image_built.to(pushing_image)
    image_pushed = pushing_image.to(image_pushed)

    def step_is_done(self):
        if self.current_state.id == self.downloading_base_image.id:
            self.base_image_downloaded()
        elif self.current_state.id == self.installing_user_pip_dependencies.id:
            self.image_built()

    def image_built(self):
        pass # set state to image_pushing