<template>
  <mdb-modal size="xl" @close="close()" cascade>

    <mdb-modal-header color="cyan lighten-1 white-text">
      <h2 class="title"><mdb-icon icon="atom" /> &nbsp;&nbsp;  <strong>{{activeDetail.name}}</strong></h2>
    </mdb-modal-header>

    <mdb-modal-body>

      <mdb-row center class="align-items-center">
        <mdb-alert class="animation fadeInDown" color="danger" v-if="isAlert" @closeAlert="isAlert = false" dismiss>
          {{ alertMessage }}
        </mdb-alert>
        <div v-else>
          <br><br>
        </div>
      </mdb-row>

      <mdb-row>

        <mdb-col col="4">
          <!-- Card -->
          <mdb-card class="map-card" style="width: 20rem">
            <!--Google map-->
            <div class="z-depth-1-half map-container" style="height: 550px">
              <iframe id="maps" ref="maps" :src="src_map" frameborder="0"
                style="border:0" allowfullscreen></iframe>
            </div>
            <!-- Card content -->
            <mdb-card-body class="px-0" :class="mapCardClosed && 'closed'" @click.native="mapCardClosed = !mapCardClosed">
              <div class="button px-2 mt-3">
                <mdb-btn color="living-coral" tag="a" floating size="lg" class="living-coral float-right"><mdb-icon icon="location-arrow" /></mdb-btn>
              </div>
              <div class="white px-4 pb-4 pt-3-5">
                <!-- Title -->
                <h5 class="card-title h5 living-coral-text">{{activeDetail.name}}</h5>
                <div class="d-flex justify-content-between living-coral-text">
                  <h6 class="card-subtitle font-weight-light">See detail <mdb-icon icon="angle-down" /></h6>
                  <!-- <h6 class="font-small font-weight-light mt-n1">25 min</h6> -->
                </div>
                <hr>
                <div class="d-flex justify-content-between pt-2 mt-1 text-center text-uppercase living-coral-text">
                  <div>
                    <i class="fas fa-compass fa-lg mb-3"></i>
                    <p class="mb-0">{{activeDetail.azimuth}}&deg;</p>
                  </div>
                  <div>
                    <i class="fas fa-drafting-compass fa-lg mb-3"></i>
                    <p class="mb-0">{{activeDetail.dip}}&deg;</p>
                  </div>
                  <div>
                    <i class="far fa-check-circle fa-lg mb-3"></i>
                    <p class="mb-0">Valid</p>
                  </div>
                </div>
                <hr>
                <table class="table table-borderless">
                  <tbody>
                    <tr>
                      <th scope="row" class="px-0 pb-3 pt-2">
                          <i class="fas fa-map-marker-alt living-coral-text"></i>
                      </th>
                      <td class="pb-3 pt-2">
                        Latitude : {{activeDetail.latitude}} <br>
                        Longitude : {{activeDetail.longitude}}
                      </td>
                    </tr>
                    <tr class="mt-2">
                      <th scope="row" class="px-0 pb-3 pt-2">
                        <i class="far fa-clock living-coral-text"></i>
                      </th>
                      <td class="pb-3 pt-2">Last updated : <br>{{ activeDetail.updated_at }}</td>
                    </tr>
                    <tr class="mt-2">
                      <th scope="row" class="px-0 pb-3 pt-2">
                        <!-- <i class="fas fa-cloud-moon living-coral-text"></i> -->
                      </th>
                      <td class="pb-3 pt-2"></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </mdb-card-body>
          </mdb-card>
        </mdb-col>

        <mdb-col col="8">
          <!-- Table with panel -->
          <mdb-card class="card narrower" cascade>
            <div class="px-4">
              <div class="table-wrapper-scroll-y my-custom-scrollbar">

                <!--Table-->
                <h4 class="card-header white cyan-text text-center py-2">{{depthReadings.length}} Depth Readings</h4> 
                <mdb-tbl class="table mb-0" responsive>
                  <!--Table head-->
                  <mdb-tbl-head>
                    <tr>
                      <th>
                        <div class="custom-control custom-checkbox">
                          <input type="checkbox" class="custom-control-input" id="checkall" v-model="checkall">
                          <label class="custom-control-label" for="checkall"><strong> No.</strong> </label>
                        </div>
                      </th>
                      <th class="th-lg"><strong> Depth </strong></th>
                      <th class="th-lg"><strong>Azimuth</strong></th>
                      <th class="th-lg"><strong>Dip</strong></th>
                      <th class="th-lg"><strong>Status</strong></th>
                    </tr>
                  </mdb-tbl-head>
                  <!--Table head-->

                  <!--Table body-->
                  <mdb-tbl-body>
                    <tr v-for="(depth, index) in depthReadings" v-bind:key="depth.id">
                      <th scope="row">
                        <div class="custom-control custom-checkbox">
                          <input class="custom-control-input" type="checkbox" :id="depth.id" :value="depth" v-model="checkedData">
                          <label class="custom-control-label" :for="depth.id">{{ index + 1 }}</label>
                        </div>
                      </th>
                      <td>{{ depth.depth }} <var>m</var></td>
                      <td>{{ depth.azimuth }}&deg;</td>
                      <td>{{ depth.dip }}&deg;</td>
                      <td>
                        <span v-bind:class="{ 
                          'badge badge-pill badge-default': depth.status == 'Trustworthy', 
                          'badge badge-pill badge-warning': depth.status == 'Untrustworthy',
                          'badge badge-pill badge-success': depth.status == 'Correct', 
                          'badge badge-pill badge-danger': depth.status == 'Incorrect'
                          }">
                          {{ depth.status }}
                        </span>
                      </td>
                    </tr>
                  </mdb-tbl-body>
                  <!--Table body-->
                </mdb-tbl>
                <!--Table-->

              </div>
            </div>
          </mdb-card>
          <!-- Table with panel -->
          <br>

          <mdb-btn outline="cyan" class="animated fadeIn" @click.native="addDepth = true" v-if="!checkedData.length && !addDepth">
            <mdb-icon icon="plus"/> Add Depth Readings
          </mdb-btn>

          <mdb-row center class="align-items-center animated fadeIn" v-if="checkedData.length">
            <strong>Is it the data Correct? &nbsp;&nbsp;</strong>
            <div class="custom-control custom-radio custom-control-inline">
              <input type="radio" name="override-value" value="Correct" 
              class="custom-control-input" id="correct-value" v-model="override">
              <label class="custom-control-label" for="correct-value">Correct</label>
            </div>
            <div class="custom-control custom-radio custom-control-inline">
              <input type="radio" name="override-value" value="Incorrect" 
              class="custom-control-input" id="incorrect-value" v-model="override">
              <label class="custom-control-label" for="incorrect-value">Incorrect</label>
            </div>
            <div class="custom-control custom-radio custom-control-inline">
              <mdb-btn color="default" @click.native="overrideData()">Override</mdb-btn>
            </div>
          </mdb-row> 

          <mdb-row center class="align-items-center animated fadeIn" v-if="addDepth && !checkedData.length">
            <mdb-col col="4">
              <mdb-input type="number" v-model="form.depth" label="Insert Depth"/>  
            </mdb-col>
            <mdb-col col="4">
              <mdb-input type="number" v-model="form.azimuth" label="Insert Azimuth"/>  
            </mdb-col>
            <mdb-col col="4">
              <mdb-input type="number" v-model="form.dip" label="Insert Dip"/>  
            </mdb-col>
          </mdb-row>     

        </mdb-col>

      </mdb-row>

    </mdb-modal-body>

    <mdb-modal-footer class="justify-content-center" v-if="addDepth && !checkedData.length">
      <mdb-btn color="light" @click.native="addDepth = false">Cancel</mdb-btn>
      <mdb-btn color="success" @click.native="add()">Save</mdb-btn>
    </mdb-modal-footer>
    <mdb-modal-footer class="justify-content-center" v-else>
      <mdb-btn color="warning" @click.native="close">Close</mdb-btn>
    </mdb-modal-footer>

  </mdb-modal>
</template>

<script>
import { 
  mdbRow,
  mdbCol,
  mdbIcon,
  mdbBtn,
  mdbModal,
  mdbModalHeader,
  mdbModalTitle,
  mdbModalBody,
  mdbModalFooter,
  mdbInput,
  mdbTextarea,
  mdbAlert,
  mdbCard,
  mdbCardImage,
  mdbCardBody,
  mdbCardTitle,
  mdbCardText,
  mdbTbl,
  mdbTblHead,
  mdbTblBody
 } from "mdbvue"
import axios from 'axios'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.xsrfCookieName = 'csrftoken'
export default {
  name: "ModalDetails",
  components: {
    mdbRow,
    mdbCol,
    mdbIcon,
    mdbBtn,
    mdbModal,
    mdbModalHeader,
    mdbModalTitle,
    mdbModalBody,
    mdbModalFooter,
    mdbInput,
    mdbTextarea,
    mdbAlert,
    mdbCard,
    mdbCardImage,
    mdbCardBody,
    mdbCardTitle,
    mdbCardText,
    mdbTbl,
    mdbTblHead,
    mdbTblBody
  },
  props: {
    activeDetail: {
      type: Object
    },
    latitude: {
        type: Number
    },
    longitude: {
        type: Number
    },
    depthsDrillHole: {
        type: Array
    }
  },
  data() {
      return {
        form: {
          drill_hole: '',
          depth: '',
          azimuth: '',
          dip: '',
          status: 'Trustworthy'
        },
        depthReadings: [],
        isAlert: false,
        alertMessage: '',
        mapCardClosed: true,
        src_map: '',
        override: '',
        checkedData: [],
        checkall: false,
        addDepth : false
      }
  },
  watch: {
    depthsDrillHole () {
      this.depthReadings = this.depthsDrillHole
    },
    latitude () {
      var src = ''.concat('https://maps.google.com/maps?q=', 
        this.latitude.toString(), ',', this.longitude.toString(), '&t=&z=13&ie=UTF8&iwloc=&output=embed')
      this.$refs.maps.contentWindow.location.replace(src)
    },
    checkall () {
      this.addDepth = false
      if (this.checkall) {
        this.checkedData = []
        this.depthReadings.map(item => this.checkedData.push(item))
      } else {
        this.checkedData = []
      }
    },
    checkedData() {
      if(!this.checkedData.length){
        this.addDepth = false
        this.checkall = false
      }
    }
  },
  methods: {
      close() {
        this.clear()
        this.$emit('close')
      },
      add() {
        var isAdd = false
        if (this.depthReadings.length == 0) {
          if (this.form.depth <= 0) {
            this.alertMessage = 'Current Depth must be greater than the surface. '
            this.isAlert = true
          } else {
            isAdd = true
          }
        } else {
          if (this.depthReadings[0].depth >= this.form.depth) {
            this.alertMessage = 'Current Depth must be greater than previous Depth. '
            this.isAlert = true
          } else {
            isAdd = true
          }
        }

        if (isAdd) {
          this.form.drill_hole = this.activeDetail.url
          axios.post('/api/v1/depthReading/', this.form).then(
            res => {
              this.clear()
            },
            error => {
              console.log(error)
            }
          )
        }
        this.addDepth = false
      },
      clear() {
        this.isAlert = false
        this.form.depth = ''
        this.form.azimuth = ''
        this.form.dip = ''
        this.override = ''
        this.checkedData =[]
        this.checkall = false
        this.loadDepthReadings()
      }, 
      loadDepthReadings () {
        axios({method: 'GET', url: '/api/v1/depthReading/?drill_hole='+this.activeDetail.id}).then(
            result => {
              this.depthReadings = result.data
            },
            error => {
              console.log(error)
            }
          )
      },
      overrideData() {
        var status = this.override
        if (status == '') {
          this.alertMessage = 'Please choose wheater Correct or Incorrect. '
          this.isAlert = true
        } else {
          var $this = this
          function getStuff(i){
            $this.checkedData[i].status = status
            axios.put('/api/v1/depthReading/'+$this.checkedData[i].id+'/', $this.checkedData[i]).then(
                res => {
                  $this.clear()
                },
                error => {
                  console.log(error)
                }
              )
          }
          for (var i = 0; i < $this.checkedData.length; i++) {
            getStuff(i)  
          }
          this.addDepth = false
        }
      }
  }
}
</script>

<style scoped>
  @import '../assets/css/map_card.css';
</style>
<style scoped>
  .my-custom-scrollbar {
    position: relative;
    height: 440px;
    overflow: auto;
  }
  .table-wrapper-scroll-y {
    display: block;
  }
</style>