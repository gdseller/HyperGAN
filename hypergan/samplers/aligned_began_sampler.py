
from hypergan.samplers.common import *

def sample_tensor(sess,generator, feed_dict, sample_file):
    if isinstance(generator, list):
        generator = generator[0]
    if generator is None:
        return
    g=tf.get_default_graph()
    with g.as_default():
        tf.set_random_seed(1)
        sample = sess.run(generator, feed_dict=feed_dict)
        #plot(self.config, sample, sample_file)
        stacks = [np.hstack(sample[x*5:x*5+5]) for x in range(1)]
        plot(config, np.vstack(stacks), sample_file)



#mask_noise = None
z = None
y = None
x = None
xb = None
def sample(gan, sample_file):
    sess = gan.sess
    config = gan.config
    global z, y, x, xb
    generator = gan.graph.g[0]
    y_t = gan.graph.y
    z_t = gan.graph.z[0] # TODO support multiple z
    x_t = gan.graph.xa
    xb_t = gan.graph.xb
    gb_t = gan.graph.gab

    if x is None:
        x = gan.sess.run(x_t)
        xb = gan.sess.run(xb_t)

    if z is None:
        z = sess.run(z_t)
        y = sess.run(y_t)


    x_file = sample_file+'x.png'
    xb_file = sample_file+'xb.png'
    autoencoded_x_file = sample_file+'autox.png'
    autoencoded_g_file = sample_file+'autog.png'
    autoencoded_hx_file = sample_file+'autohx.png'
    autoencoded_hg_file = sample_file+'autohg.png'
    autoencoded_rxabba_file = sample_file+'autorxabba.png'
    autoencoded_rxbaab_file = sample_file+'autorxbaab.png'
    ga_file = sample_file+'ga.png'
    gb_file = sample_file+'gb.png'
    feed_dict = {z_t: z, y_t: y, x_t: x, xb_t: xb}
    sample_tensor(sess,generator, feed_dict, sample_file)
    print(x_t)
    print("GAAAA", gan.graph.ga)
    sample_tensor(sess,gan.graph.xa, feed_dict, x_file)
    sample_tensor(sess,gan.graph.xb, feed_dict, xb_file)
    sample_tensor(sess,gan.graph.xba, feed_dict, autoencoded_x_file)
    sample_tensor(sess,gan.graph.xab, feed_dict, autoencoded_hg_file)
    sample_tensor(sess,gan.graph.xabba, feed_dict, autoencoded_g_file)
    sample_tensor(sess,gan.graph.xbaab, feed_dict, autoencoded_hx_file)
    sample_tensor(sess,gan.graph.rxabba, feed_dict, autoencoded_rxabba_file)
    sample_tensor(sess,gan.graph.rxbaab, feed_dict, autoencoded_rxbaab_file)
    samples = []
    samples.append({'image':x_file, 'label':'xa'})
    samples.append({'image':xb_file, 'label':'xb'})

    samples.append({'image':autoencoded_hg_file, 'label':'xab'})
    samples.append({'image':autoencoded_x_file, 'label':'xba'})
    samples.append({'image':autoencoded_g_file, 'label':'xabba'})
    samples.append({'image':autoencoded_hx_file, 'label':'xbaab'})
    samples.append({'image':autoencoded_rxabba_file, 'label':'rxabba'})
    samples.append({'image':autoencoded_rxbaab_file, 'label':'rxbaab'})
    sample_tensor(sess,gan.graph.ga, feed_dict, ga_file)
    sample_tensor(sess,gan.graph.gab, feed_dict, gb_file)
    samples.append({'image':ga_file, 'label':'ga'})
    samples.append({'image':gb_file, 'label':'gb'})
    #samples.append({'image':autoencoded_gb_file, 'label':'rxa'})
    #samples.append({'image':autoencoded_xb_file, 'label':'rgabba'})

    return samples