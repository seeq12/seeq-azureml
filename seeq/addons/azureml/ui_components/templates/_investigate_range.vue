<template>
  <div
      class="d-flex flex-column ml-5 mr-5"
      :style="investigation_range_visible? '': 'display: none !important;'"
  >
    <div class="d-flex flex-row justify-space-between" style="max-width: 270px;"
    >
      <div style="width: 50px;">
        Start:
      </div>
      <div class="ml-5 mb-5" style="width: 200px; border: 1px solid #000000;">
        <jupyter-widget :widget="start_range"/>
      </div>
    </div>
    <div class="d-flex flex-row justify-space-between" style="max-width: 270px;"
    >
      <div style="width: 50px;">
        End:
      </div>
      <div class="ml-5 mb-5" style="width: 200px; border: 1px solid #000000;">
        <jupyter-widget :widget="end_range"/>
      </div>
    </div>
  </div>

</template>

