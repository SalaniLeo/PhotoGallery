<script lang="ts">
	import { isUserLogged, refreshPosts, showCreatePost } from '$lib/stores';
	import CreatePost from '$lib/components/createPost.svelte';
	import Posts from '$lib/components/posts.svelte';
	import { goto } from '$app/navigation';
	export let data;
	let unique = {};

	refreshPosts.subscribe((b) => {
		unique = {};
	});
</script>

<div class="root">
	<div class="content">
		<div class="top">
			{#if $isUserLogged}
				<p>Hi, {data.user?.name}!</p>
				{#if data.user?.admin}
					<button on:click={() => showCreatePost.set(true)}>Create Post</button>
				{/if}
				<button on:click={() => goto('/profile')}>Profile</button>
			{/if}
		</div>
		<div class="center">
			{#key unique}
				<Posts {data} />
			{/key}
		</div>
	</div>
	<CreatePost />
</div>

<style>
	.content {
		display: flex;
		align-items: center;
		justify-self: center;
		flex-direction: column;
		width: 100%;
	}
	.top {
		margin-bottom: 1rem;
	}
</style>
