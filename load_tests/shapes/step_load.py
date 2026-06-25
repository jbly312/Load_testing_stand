from locust import LoadTestShape

class StepLoadTest(LoadTestShape):

    step_time = 30
    step_users = 50
    spawn_rate = 20
    max_users = 500

    def tick(self):

        run_time = self.get_run_time()

        current_step = run_time//self.step_time
        users = (current_step+1) * self.step_users

        if users > self.max_users:
            return None

        return (users, self.spawn_rate)

