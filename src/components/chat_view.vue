<template>
    <a-spin :spinning="spinning">
        <a-list v-if="comments.length" :data-source="comments"
            :header="`${comments.length} ${comments.length > 1 ? 'replies' : 'reply'}`" item-layout="horizontal">
            <template #renderItem="{ item }">
                <a-list-item>
                    <a-comment :author="item.author" :avatar="item.avatar">
                        <template #actions>
                            <span v-for="(action, index) in item.actions" :key="index">{{ action }}</span>
                        </template>
                        <template #content>
                            <MdEditor v-model="item.content" previewOnly />
                        </template>
                        <template #datetime>
                            <span>{{ item.datetime }}</span>
                        </template>
                    </a-comment>
                </a-list-item>
            </template>
        </a-list>
    </a-spin>
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
            <div>
                <a-button type="primary" @click="showModal">修改token</a-button>
                <a-modal v-model:visible="visible" title="修改token" @ok="handleOk">
                    <a-textarea v-model:value="value1" placeholder="Basic usage" :rows="4" />
                </a-modal>
                <a-button type="primary" @click="changeStyle('balanced')">切换至平衡模式</a-button>
                <a-button type="primary" @click="changeStyle('creative')">切换至创造模式</a-button>
                <a-button type="primary" @click="changeStyle('precise')">切换至严格模式</a-button>
                
            </div>
        </template>
    </a-comment>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
import dayjs from 'dayjs';
import axios, { AxiosResponse } from "axios"
import relativeTime from 'dayjs/plugin/relativeTime';
dayjs.extend(relativeTime);
import MdEditor from 'md-editor-v3';
import 'md-editor-v3/lib/style.css';
var ws = new WebSocket("ws://localhost:8000/api/ws");
type Comment = Record<string, string>;
import { message } from 'ant-design-vue';
import "ant-design-vue/es/message/style/css"
const child = ref(null)

export default defineComponent({
    async mounted() {
        if (window.localStorage.getItem("token") == null) {
            message.error("未配置token!")
            console.log(this.token)
        } else {
            let token = window.localStorage.getItem("token")
            let chat = await axios.post("/api/newchat", {
                "cookie": token,
                "style": "balanced"
            })
            this.chat_data = chat.data;
            message.success("成功连接服务器")
        }
    },
    components: {
        MdEditor
    },
    methods: {
        getChatData() {
            console.log(this.chat_data)
        },
        setChatData() {

        },
        async handleOk() {
            let data = [
                {
                    "name": "_U",
                    "value": this.value1
                }
            ]
            window.localStorage.setItem("token", JSON.stringify(data))
            let chat = await axios.post("/api/newchat", {
                "cookie": data,
                "style": "balanced"
            })
            this.chat_data = chat.data;
            this.visible = false;
        },
        handleSubmit() {
            if (!this.value) {
                return;
            }

            this.submitting = true;

            setTimeout(() => {
                this.submitting = false;
                this.comments = [
                    ...this.comments,
                    {
                        author: 'User',
                        avatar: '/assets/user.png',
                        content: this.value,
                        datetime: dayjs().fromNow(),
                    },
                ];
                this.value = '';
            }, 100);
            ws.send(JSON.stringify({ "id": this.chat_data["id"], "message": this.value }))
            this.spinning = !this.spinning;
            //ws.send(value.value);
            //ws.send({"id": })
        },
        async changeStyle(style: string){
            let response = await axios.post("/api/change_style",{
                "id": this.chat_data["id"],
                "style": style
            })
            message.success(`成功切换对话风格:${style}`)
        }
    },
    setup() {
        const visible = ref<boolean>(false);
        const value1 = ref<string>('');
        const showModal = () => {
            visible.value = true;
        };
        const spinning = ref<boolean>(false);
        const comments = ref<Comment[]>([]);
        const submitting = ref<boolean>(false);
        const value = ref<string>('');
        let token = ref(null)
        let chat_data = {
            "id": null
        }
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
            spinning.value = !spinning.value;
        };

        return {
            comments,
            submitting,
            value,
            token,
            visible,
            showModal,
            value1,
            chat_data,
            spinning
        };
    },
});
</script>
  
  