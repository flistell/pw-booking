<script setup>
</script>

<template>
    <div id="bw_main">
        <div id="bw_row" class="row align-items-start">
            <div id="bw_r1c1" class="card col-lg-4 sticky p-lg-0">
                <ItemCardSmall :brand="item.item_details.brand" :model="item.item_details.model"
                    :photo="item.item_details.photo" />
            </div>
        </div>
    </div>
</template>