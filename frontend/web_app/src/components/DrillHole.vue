<template>

    <div class="media mt-1">
      <h3 class="h3-responsive font-weight-bold mr-3 pt-0">{{index+1}}</h3>
      <div class="media-body mb-3">
        <h6 class="mt-0 font-weight-bold">{{name}}</h6>
        <hr class="hr-bold my-2">
        <p class="font-smaller">
          <mdb-icon icon="map-marker-alt"/>&nbsp;
          {{latitude}}, {{longitude}}
        </p>
        <p><small><em>Last Updated: {{updated_at}}</em></small></p>
      </div>
      <div class="media-body mb-3">
        <mdb-btn @click.native="getDetail" tag="a" color="cyan lighten-2" floating size="lg" class="ml-4">
          <mdb-icon fab icon="telegram-plane" /> Detail
        </mdb-btn>
      </div>
    </div>

</template>

<script>
import { mdbBadge, mdbIcon, mdbBtn } from "mdbvue"
import axios from 'axios'
export default {
  name: "DrillHole",
  components: {
    mdbBadge,
    mdbIcon,
    mdbBtn
  },
  props: {
    index: {
      type: Number
    },
    id: {
      type: String
    },
    url: {
      type: String
    },
    name: {
      type: String
    },
    latitude: {
      type: Number
    },
    longitude: {
      type: Number
    },
    dip: {
      type: Number
    },
    azimuth: {
      type: Number
    },
    created_at: {
      type: String
    },
    updated_at: {
      type: String
    }
  },
  data() {
    return {
      drill_hole: {},
      depth_readings: []
    }
  },
  methods: {
    getDetail() {
      axios({method: 'GET', url: '/api/v1/drillHole/'+this.id+'/'}).then(
        result => {
          this.drill_hole = result.data
          axios({method: 'GET', url: '/api/v1/depthReading/?drill_hole='+this.id}).then(
            result => {
              this.depth_readings = result.data
              this.$emit("detail", this.drill_hole, this.depth_readings)
            },
            error => {
              console.log(error)
            }
          )
        },
        error => {
          console.log(error)
        }
      )
    }
  }
}
</script>