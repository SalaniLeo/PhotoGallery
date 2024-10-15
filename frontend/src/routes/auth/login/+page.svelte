<script lang="ts">
	import PostView from './../../../lib/components/postView.svelte';
	let email = '',
		password = '',
		error = '';

	export let form;
	export let data;
</script>

<form method="POST">
	<div class="root">
		<div class="container">
			<div class="left">
				<h2>Log In</h2>
				<div class="content">
					<div class="inputs">
						<input
							type="text"
							id="email"
							name="email"
							placeholder="Email"
							style="border-bottom: 2px solid {form?.state};"
							bind:value={email}
						/>
						<input
							type="password"
							id="password"
							name="password"
							placeholder="Password"
							style="border-bottom: 2px solid {form?.state};"
							bind:value={password}
						/>
					</div>
					<div class="errorslot">
						{#if form?.error}
							<small style="color: {form?.state};">{form?.error}</small>
						{/if}
					</div>
					<div class="oauth"></div>
				</div>
				<div class="signin">
					<p><a href="/auth/register">Sign In</a> to create an account</p>
				</div>
				<div class="ralign">
					<button type="submit">Log In</button>
				</div>
			</div>
			<div class="right">
				<!-- <LatestPost {data}></LatestPost> -->

				<PostView post={data.latest_post} imageOnly={true} useAnalytics={false}></PostView>
			</div>
		</div>
	</div>
</form>

<style>
	p {
		margin: 0;
	}
	.root {
		padding: 25px;
		display: flex;
		justify-content: center;
		align-items: center;
	}
	.container {
		padding: 0px;
		width: unset;
		height: fit-content;
		border-radius: var(--border-radius-heavy);
		border: 2px solid var(--border-color);
		background-color: var(--background-blurry);
		display: flex;
		flex-direction: row;
		overflow: hidden;
	}
	.container > .left {
		padding: 1rem;
		width: 40%;
		min-width: 250px;
		display: flex;
		flex-direction: column;
		gap: 10px;
	}
	.container > .right {
		width: unset;
		display: flex;
		align-items: center;
		padding: 1rem;
	}
	.left > .content {
		height: 100%;
		display: flex;
		flex-direction: column;
		gap: 20px;
		align-items: unset;
		justify-self: unset;
	}
	.left > .content > .errorslot {
		height: 0px;
		transform: translateY(-12.5px);
	}
	.left > .content > .inputs {
		display: flex;
		flex-direction: column;
		gap: 20px;
	}
	.left > .content > .oauth {
		display: flex;
		flex-direction: column;
		gap: 20px;
	}
	.left h3 {
		margin: 15px;
	}
	.ralign {
		display: flex;
		justify-content: right;
		align-items: center;
	}
	@media screen and (max-width: 1200px) {
		.root {
			display: flex;
			flex-direction: row;
			overflow: hidden;
			width: unset;
			margin-left: 2rem;
			margin-right: 2rem;
		}
	}
	@media screen and (max-width: 1000px) {
		/* .right{
		display: none;
	} */
	}
	@media screen and (max-width: 720px) {
		.root {
			margin-left: 0.5rem;
			margin-right: 0.5rem;
		}
		.right {
			display: none !important;
		}
		.container {
			width: 100%;
		}
		.left {
			width: 100% !important;
		}
	}
</style>
