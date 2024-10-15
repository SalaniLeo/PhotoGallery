<script lang="ts">
	import { isUserLogged, rootData, showCreatePost } from '$lib/stores';
	import PostView from '$lib/components/postView.svelte';
	import Upload from '$lib/components/upload.svelte';

	let columnView = true;
	let gridView = false;
</script>

<div class="root">
	<div class="content flexcolumn gap-large">
		<div class="topbar flexrow space-between">
			<div class="start">
				{#if $isUserLogged}
					{#if $rootData.user.info.admin}
						<Upload data={$rootData}></Upload>
						<button class="fit-content padding2" on:click={() => showCreatePost.set(true)}
							><i class="fa-solid fa-plus"></i> Create Post</button
						>
					{/if}
				{/if}
			</div>
			<div class="end flexrow gap-moderate valign view-selector notransition">
				<div class="secondary">View:</div>
				<div class="view-buttons blurry outline-normal valign radius-medium">
					<button
						class="transparent padding2"
						class:button-active={gridView}
						on:click={() => {
							columnView = false;
							gridView = true;
						}}><i class="fa-solid fa-grip"></i></button
					>
					<button
						class="transparent padding2"
						class:button-active={columnView}
						on:click={() => {
							columnView = true;
							gridView = false;
						}}><i class="fa-solid fa-list"></i></button
					>
				</div>
			</div>
		</div>
		<div class="posts-container" class:gridView class:columnView>
			{#each $rootData.posts as post, index}
				<div class="post-wrapper">
					<PostView {post} imageOnly={false} showButtons={true} {index} showActions={true}
					></PostView>
				</div>
			{/each}
		</div>
	</div>
</div>

<style>
	.root {
		padding: 0 !important;
	}
	.topbar {
		padding-left: 12rem;
		padding-right: 12rem;
	}
	.gridView {
		justify-content: center;
		align-items: center;
		display: flex;
		gap: 1rem !important;
		flex-direction: row;
		flex-wrap: wrap;
	}
	.columnView {
		display: flex;
		flex-direction: column;
		flex-wrap: wrap;
	}
	.post-wrapper {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}
	.posts-container {
		gap: 2rem;
		align-items: center;
		transition-duration: 0s !important;
	}
	@media screen and (max-width: 1100px) {
		.view-selector {
			visibility: hidden;
		}
	}
	@media screen and (max-width: 1000px) {
		.posts-container {
			display: unset;
			padding: 0;
			margin: 0;
		}
		.columnView {
			align-items: unset;
		}
	}
	@media screen and (max-width: 720px) {
		.posts-container {
			margin-left: 0.5rem;
			margin-right: 0.5rem;
		}
	}
</style>
