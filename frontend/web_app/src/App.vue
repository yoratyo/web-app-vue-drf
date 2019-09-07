<template>
  <mdb-container>
    <br><br>
    <mdb-row>
      <mdb-col col="3">
        <img src="./assets/logo.png" class="img-fluid" alt="Logo">
        <br><br>
        <dd class="text-uppercase my-3 text-center">There is <strong> {{drill_holes.length}} </strong> Drill Holes</dd>
      </mdb-col>

      <mdb-col col="9">
        <h2 class="text-uppercase my-1">List of Drill Hole:</h2>
        
        <form class="form-inline md-form form-sm mt-2">
            <mdb-input label="Search by Name" v-model="searchKey" icon="fas fa-search"/>
        </form>
       
        <DrillHole
          v-for="(drill_hole, index) in filteredDrill_holes"
          :index="index"
          :id="drill_hole.id.toString()"
          :url="drill_hole.url"
          :name="drill_hole.name"
          :latitude="drill_hole.latitude"
          :longitude="drill_hole.longitude"
          :dip="drill_hole.dip"
          :azimuth="drill_hole.diazimuthp"
          :created_at="drill_hole.created_at"
          :updated_at="drill_hole.updated_at"
          :key="drill_hole.id"
          @detail="showModal"
        />
      </mdb-col>
      
    </mdb-row>

    <ModalDetails
      v-show="isModalVisible"
      :activeDetail="activeDetail"
      :latitude="activeLat"
      :longitude="activeLong"
      :depthsDrillHole="depthsDrillHole"
      @close="closeModal"
    />

  </mdb-container>
</template>

<script>
import axios from 'axios'
import { error } from 'util'
import DrillHole from "@/components/DrillHole"
import ModalDetails from "@/components/ModalDetails"
import {
  mdbContainer,
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
  mdbTextarea
} from "mdbvue"
export default {
  name: "App",
  components: {
    mdbContainer,
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
    DrillHole,
    ModalDetails
  },
  data() {
    return {
      searchKey: '',
      drill_holes : [],
      isModalVisible: false,
      activeDetail: {},
      activeLat: -6.2407743,
      activeLong: 107.033378,
      depthsDrillHole: []
    }
  },
  mounted() {
    this.getDrillHoles()
  },
  methods: {
    getDrillHoles() {
      axios({method: 'GET', url: '/api/v1/drillHole/'}).then(
        result => {
          this.drill_holes = result.data
        },
        error => {
          console.log(error)
        }
      )
    },
    showModal(activeDetail, depthsDrillHole) {
      this.activeDetail = activeDetail
      this.activeLat = activeDetail.latitude
      this.activeLong = activeDetail.longitude
      this.depthsDrillHole = depthsDrillHole
      this.isModalVisible = true
    },
    closeModal() {
      this.getDrillHoles()
      this.isModalVisible = false
    }
  },
  computed: {
    filteredDrill_holes: function(){
      return this.drill_holes.filter((drill_hole) => {
        return drill_hole.name.toLowerCase().match(this.searchKey.toLowerCase())
      })
    }
  }
}
</script>