<template>
  <div class="container">
    <h2>FarmBot</h2>
    <alert
      v-if="showMessage"
      :message="msg"
      :status="status"
    />
    <div class="row">
      <div class="col-sm-10">
        <br>
        <button
          type="button"
          class="btn btn-success btn-sm"
          @click="getLogs()"
        >
          View logs
        </button>
        <button
          type="button"
          class="btn btn-warning btn-sm"
        >
          Check weather
        </button>
        <button
          type="button"
          class="btn btn-danger btn-sm"
          @click="toggleDevice(false, 'all')"
        >
          Stop all
        </button>
        <br>
        <br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">
                Device
              </th>
              <th scope="col">
                Pin
              </th>
              <th scope="col">
                Active
              </th>
              <th scope="col">
                Weather
              </th>
              <th />
              <th scope="col">
                Time schedule
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(device, index) in devices"
              :key="index"
            >
              <td>{{ device.name }}</td>
              <td>{{ device.pin }}</td>

              <td>
                <span v-if="device.is_on">Yes</span>
                <span v-else>No</span>
              </td>
              <td>
                <span v-if="device.weather_dependent">Yes</span>
                <span v-else>No</span>
              </td>
              <td>
                <button
                  type="button"
                  class="btn btn-success btn-sm"
                  @click="toggleDevice(true, device.id)"
                >
                  Start
                </button>

                <button
                  type="button"
                  class="btn btn-success btn-sm"
                >
                  A
                </button>
                <button
                  type="button"
                  class="btn btn-warning btn-sm"
                >
                  U
                </button>
                <button
                  type="button"
                  class="btn btn-danger btn-sm"
                >
                  D
                </button>
              </td>
              <td colspan="5">
                <table class="table">
                  <thead>
                    <tr>
                      <th scope="col">
                        Start
                      </th>
                      <th scope="col">
                        End
                      </th>
                      <th scope="col">
                        Frequency(days)
                      </th>
                      <th />
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="(ts) in device.time"
                      :key="ts.id"
                    >
                      <td>{{ ts.start }}</td>
                      <td>{{ ts.stop }}</td>
                      <td>{{ ts.skip_days }}</td>
                      <td>
                        <button
                          type="button"
                          class="btn btn-warning btn-sm"
                        >
                          U
                        </button>
                        <button
                          type="button"
                          class="btn btn-danger btn-sm"
                        >
                          D
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div
      v-if="showLogsModal"
      id="logs-modal"
      class="modal d-block"
      role="dialog"
      aria-modal="true"
      aria-labelledby="logs-modal-title"
      @click.self="showLogsModal = false"
    >
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5
              id="logs-modal-title"
              class="modal-title"
            >
              Log viewer
            </h5>
            <button
              type="button"
              class="btn-close"
              aria-label="Close"
              @click="showLogsModal = false"
            />
          </div>
          <div class="modal-body">
            <textarea
              id="txtMessage"
              class="form-control"
              :value="logs"
              rows="10"
              readonly
            />
          </div>
        </div>
      </div>
      <div class="modal-backdrop show" />
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
    name: 'DeviceSchedule',
    components: {
      alert: Alert
    },
    data() {
        return {
            devices: [],
            url: 'http://localhost:5000',
            msg: '',
            showMessage: false,
            status: '',
            logs: '',
            showLogsModal: false,
        };
    },
    created() {
        this.getSchedule();
    },
    methods: {
        getSchedule() {
          const path = `${this.url}/schedule`;
          axios.get(path)
              .then((res) => {
                  this.devices = res.data.devices;
              })
              .catch((error) => {
                  console.error(error);
              });
        },
        getLogs() {
          const path = `${this.url}/logs`;
          axios.get(path)
              .then((res) => {
                  this.logs = res.data.logs;

                  this.showLogsModal = true;
              })
              .catch((error) => {
                  console.error(error);
              });
        },
        toggleDevice(start, id) {
          const path = `${this.url}/toggle_device`;
          axios.post(path, { id, should_start: `${start}` })
              .then((res) => {
                  this.msg = `${res.data.status} Device ${id} ${start ? 'started' : 'stopped'}`;
                  this.showMessage = true;
                  this.status = 'success';
              })
              .catch((error) => {
                  console.error(error);
              });
        },
    },
};
</script>

<style scoped>
.modal-dialog {
  z-index: 1055;
}
</style>
