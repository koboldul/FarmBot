<template>
  <div class="container">
    <h2>FarmBot</h2>
    <alert :message="msg" v-if="showMessage" :status="status" />
    <div class="row">
      <div class="col-sm-10">
        <br>
        <button type="button" class="btn btn-success btn-sm"
        @click="getLogs()">View logs</button>
        <button type="button" class="btn btn-warning btn-sm">Check weather</button>
        <button type="button" class="btn btn-danger btn-sm"
           @click="toggleDevice(false, 'all')">Stop all</button>
        <br>
        <br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Device</th>
              <th scope="col">Pin</th>
              <th scope="col">Active</th>
              <th scope="col">Weather</th>
              <th></th>
              <th scope="col">Time schedule</th>

            </tr>
          </thead>
          <tbody>
            <tr v-for="(device, index) in devices" :key="index">
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
                <button type="button" class="btn btn-success btn-sm"
                 @click="toggleDevice(true, device.id)">
                  Start
                </button>

                <button type="button" class="btn btn-success btn-sm">A</button>
                <button type="button" class="btn btn-warning btn-sm">U</button>
                <button type="button" class="btn btn-danger btn-sm">D</button>
              </td>
            <td colspan="5">
              <table class="table">
                            <thead>
                            <tr>
                              <th scope="col">Start</th>
                              <th scope="col">End</th>
                              <th scope="col">Frequency(days)</th>
                              <th></th>
                            </tr>
                            </thead>
                            <tbody>
                              <tr v-for="(ts) in device.time" :key="ts.id">
                                <td>{{ ts.start }}</td>
                                <td>{{ ts.stop }}</td>
                                <td>{{ ts.skip_days }}</td>
                                <td>
                                  <button type="button" class="btn btn-warning btn-sm">U</button>
                                  <button type="button" class="btn btn-danger btn-sm">D</button>
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
    <b-modal ref="viewLogsModal"
             id="logs-modal"
             title="Log viewer"
             
             hide-footer>
        <b-form-textarea id="txtMessage"
                     plaintext :value="logs"
                     placeholder=""
                     :rows="10"
                     :max-rows="100">
        </b-form-textarea>

    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert'
import TextViewer from './TextViewer'

export default {
    data() {
        return {
            devices: [],
            url: 'http://localhost:5000',
            msg: '',
            showMessage: false,
            status: '',
            logs: ''
        };
    },
    components: {
      alert: Alert
    },
    methods: {
        getSchedule() {
          const path = `${this.url}/schedule`;
          axios.get(path)
              .then((res) => {
                  this.devices = res.data.devices;
              })
              .catch((error) => {
                  // eslint-disable-next-line
                  console.error(error);
              });
        },
        getLogs() {
          const path = `${this.url}/logs`;
          axios.get(path)
              .then((res) => {
                  this.logs = res.data.logs;

                  this.$refs.viewLogsModal.show();
              })
              .catch((error) => {
                  // eslint-disable-next-line
                  console.error(error);
              });
        },
        toggleDevice(start, id) {
          const path = `${this.url}/toggle_device`;
          axios.post(path, {"id": id, "should_start": `${start}`})
              .then((res) => {
                  this.msg = `${res.data.status} Device ${id} ${start ? 'started':'stopped'}`;
                  this.showMessage = true
                  this.status = 'success'
              })
              .catch((error) => {
                  // eslint-disable-next-line
                  console.error(error);
              });
        },
    },
    created() {
        this.getSchedule();
    },
}
</script>
