<script lang="ts">
	import PostView from '$lib/components/postView.svelte';
	import Upload from '$lib/components/upload.svelte';
	import { isUserLogged, showCreatePost } from '$lib/stores';

	/** @type {import('./$types').PageData} */
	export let data;
</script>

<div class="root">
	<div class="content flexcolumn space-between">
		<div class="intro flexcolumn vstartalign">
			<div class="title flexrow valign gap-medium" style="width: 100%;">
				{#if $isUserLogged}
					<h1>Welcome back, {data.user.info.firstname}!</h1>
					<!-- <button on:click={() => goto('/profile')}>Profile</button> -->
				{:else}
					<h1>Welcome!</h1>
				{/if}
			</div>
			<p>
				This website is a collection of the most beautiful photos I took. It's open source on <a
					href="https://www.github.com/SalaniLeo">GitHub</a
				> and self hostable with docker.
			</p>
			<!-- <h2>Want to take a look at website statistics?</h2>
			<p>
				Go to <a href="/statistics">statistics</a> page to take a look!
			</p>
			<h2>Interested in my work?</h2>
			<p>
				Contact me on <a href="https://me.salanileo.dev">any of these socials</a>
				or via my <a href="mailto:leonardo07.salani@gmail.com">email</a>
			</p> -->
		</div>
		<div class="posts gap-moderate flexcolumn">
			<div class="mostLiked">
				<h2>Most liked post:</h2>
				<PostView useAnalytics={false} post={data.most_liked_post[0]} imageOnly={false}></PostView>
			</div>
			<div class="mostViewed">
				<h2>Most viewed post:</h2>
				<PostView useAnalytics={false} post={data.most_viewed_post[0]} imageOnly={false}></PostView>
			</div>
			<div class="latestPost">
				<h2>Latest post:</h2>
				<PostView useAnalytics={false} post={data.latest_post} imageOnly={false}></PostView>
			</div>
		</div>
	</div>
</div>

<style>
	p {
		margin: 0.5rem;
	}
	.root {
		display: flex;
		justify-content: center;
		align-items: center;
		padding: 1rem;
		padding-top: 0 !important;
	}
	.content {
		width: 100%;
		/* border-radius: var(--border-radius-heavy); */
		max-width: 88rem;
		gap: 1.5rem;
		/* background-color: var(--background-blurry); */
	}
	.intro {
		max-width: 42rem;
		gap: 0.5rem;
		text-align: left;
	}
	h1,
	h2,
	h3,
	p {
		margin: 0.5rem;
	}
</style>
