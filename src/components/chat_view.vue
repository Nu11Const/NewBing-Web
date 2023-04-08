<template>
    <a-list v-if="comments.length" :data-source="comments"
        :header="`${comments.length} ${comments.length > 1 ? 'replies' : 'reply'}`" item-layout="horizontal">
        <template #renderItem="{ item }">
            <a-list-item>
                <a-comment :author="item.author" :avatar="item.avatar" :content="item.content" :datetime="item.datetime" />
            </a-list-item>
        </template>
    </a-list>
    <a-comment>
        <template #avatar>
            <a-avatar src="/assets/user.png" alt="User" />
        </template>
        <template #content>
            <a-form-item>
                <a-textarea v-model:value="value" :rows="4" />
            </a-form-item>
            <a-form-item>
                <a-button html-type="submit" :loading="submitting" type="primary" @click="handleSubmit">
                    提交
                </a-button>
            </a-form-item>
        </template>
    </a-comment>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
dayjs.extend(relativeTime);
var ws = new WebSocket("ws://localhost:8000/api/ws");
type Comment = Record<string, string>;

export default defineComponent({
    setup() {
        const comments = ref<Comment[]>([]);
        const submitting = ref<boolean>(false);
        const value = ref<string>('');
        const handleSubmit = () => {
            if (!value.value) {
                return;
            }

            submitting.value = true;

            setTimeout(() => {
                submitting.value = false;
                comments.value = [
                    ...comments.value,
                    {
                        author: 'User',
                        avatar: '/user.png',
                        content: value.value,
                        datetime: dayjs().fromNow(),
                    },
                ];
                value.value = '';
            }, 100);
            ws.send(value.value);
        };
        ws.onmessage = function (event) {
            comments.value = [
                    ...comments.value,
                    {
                        author: 'Bing',
                        avatar: '/bing.svg',
                        content: event.data,
                        datetime: dayjs().fromNow(),
                    },
                ];
        };

        return {
            comments,
            submitting,
            value,
            handleSubmit,
        };
    },
});
</script>
  
  